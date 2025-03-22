import React, { useState, useEffect} from "react";
import apiClient from "../../utilities/apiClient";
import Select from "react-select";
import {GenerateErrorDisplayElement} from "../../utilities/Error";
import fetchProtectedFile from "../../utilities/fetchProtectedFile";

interface Translation {
    id: number;
    document: string;
    customer: {id:number, first_name:string, last_name:string};
    language: {id:number, language_name:string};
    word_count: number;
    company: string;
    notes: string;
}

function TranslationsCreationPage() {

    const [uploaddocument, setuploadDocument] = useState<File | null>(null);
    const [word_count, setWordCount] = useState('');
    const [language, setLanguage] = useState<{ value: string; label: string } | null>(null);
    const [notes, setNotes] = useState('');
    const [languageOptions, setLanguageOptions] = useState([]);
    const [company, setCompany] = useState('');
    const [errorElm, setErrorElm] = useState(<div></div>);
    const [translations, setTranslations] = useState<Translation[] | null>(null);

    const clearForm = () => {
        setuploadDocument(null);
        setWordCount('');
        setLanguage(null);
        setNotes('');
    }

    const fetchTranslations = () => {
        apiClient.get("/translations/")
            .then((res) => {
                if (res.data.status == "success") {
                    console.log(res.data.result.result)
                    setTranslations(res.data.result.result);
                } else if (res.data.status == "error") {
                    setErrorElm(GenerateErrorDisplayElement(res.data.error));
                }
            })
            .catch((err) => {
                setErrorElm(GenerateErrorDisplayElement(err.response?.data.error));
            });
    };

    const fetchData = () => {
        apiClient.get("/languages/")
            .then((res) => {
                if (res.data.status == "success") {
                    console.log("Language Retrieval Successful:", res.data);
                    const formattedOptions = res.data.result.languages.map((lang:string) => ({
                        value: lang,
                        label: lang,
                    }));
                    setLanguageOptions(formattedOptions);
                } else if (res.data.status == "error") {
                    setErrorElm(GenerateErrorDisplayElement(res.data.error));
                }
            })
            .catch((err) => {
                setErrorElm(GenerateErrorDisplayElement(err.response?.data.error));
            });
    };

    useEffect(() => {
            fetchTranslations();
            fetchData();

        }, []);
    
    const submitTranslationCreation = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        console.log("Submitting translation form")

        if (!document) {
            console.error("No document selected.");
            return;
        }

        if (!language) {
            console.error("No language selected.");
            return;
        }
        
        const reader = new FileReader();

        if (uploaddocument) {
            reader.readAsDataURL(uploaddocument);  // Convert file to base64
        
            reader.onloadend = async () => {
                const base64File = reader.result?.toString();
                const document_name= uploaddocument.name;
                const returnData = {
                    document_name :document_name,
                    document: base64File,
                    word_count: word_count,
                    language: language.value,
                    company: company,
                    notes: notes,
                };
            
                try {
                    const response = await apiClient.post("/translation-request/", returnData, {
                        headers: {
                            "Content-Type": "application/json",  // Send as JSON
                        },
                    });
        
                    console.log("Translation Creation Successful:", response.data);
                    clearForm();
                    fetchTranslations();
                } catch (error: unknown) {
                    if (error instanceof Error) {
                        console.error("Translation Creation Error:", error.message);
                    } else {
                        console.error("An unknown error occurred.");
                    }
                }      
            }     
        };

    }

    return (
        <>
        <div className="main-container container">
            <div className="d-flex">
                <div className="col-4">
                    <h4>Request a New Translation</h4>
                    <form className="form" onSubmit={submitTranslationCreation}>
                        <div className="mb-2">
                            <label className="form-label">Document:</label>
                                <input
                                    className="form-control" 
                                    type="file"
                                    onChange={(e) => setuploadDocument(e.target.files?.[0] || null)} 
                                    required
                                />
                        </div>

                        <div className="mb-2">
                            <label className="form-label">Word Count:</label>
                            <input 
                                className="form-control"
                                type="number"
                                value={word_count}
                                onChange={(e)=>setWordCount(e.target.value)}
                                required
                            />
                        </div>

                        <div className="mb-2">
                            <label className="form-label">Language</label>
                            <Select
                                options={languageOptions}
                                value={language}
                                onChange={(selectedOption) => setLanguage(selectedOption)}
                                placeholder="Type to search languages..."
                                required
                            />
                        </div>

                        <div>
                                <label>Company:</label>
                                <input
                                    className="form-control"
                                    type="text"
                                    value={company}
                                    onChange={(e) => setCompany(e.target.value)}
                                />
                            </div>

                       

                        <div className="mb-3">
                            <label className="form-label">Notes/Description:</label>
                            <textarea
                                className="form-control"
                                value={notes}
                                onChange={(e) => setNotes(e.target.value)}
                            />
                        </div>

                        <button className="btn btn-primary" type="submit">Request Appointment</button>
                        {errorElm}
                    </form>
                </div>
                <div className="col ms-3">
                    <h4>Your Translations</h4>
                    <div className="d-flex">
                    {translations && translations.map((translation, index) => {
                            let filename: string = translation.document.replace("/media/translation_documents/", ""); 
                            return (
                                <div key={index} className="card row-xs m-1">
                                    <ul className="list-group list-group-flush">
                                        <li className="list-group-item">Customer: <h5 className="card-title">{translation.customer.first_name} {translation.customer.last_name}</h5></li>
                                        <li className="list-group-item">Language: {translation.language.language_name}</li>
                                        <li className="list-group-item">Word count: {translation.word_count}</li>
                                        <li className="list-group-item">Company: {translation.company}</li>
                                        <li className="list-group-item"><strong>Document:</strong> <button className="btn btn-link p-0" onClick={() => fetchProtectedFile(filename)}><i className="bi bi-download me-2"></i>{filename}</button></li>
                                    </ul>
                                </div>
                            )}
                        )
                    }
                    {(translations && translations?.length == 0) && <p>No translations requested!</p>}
                    </div>
                </div>
            </div>
        </div>

        </>
    );
}

export default TranslationsCreationPage;