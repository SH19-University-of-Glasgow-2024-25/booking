import { useEffect, useState } from "react";
import apiClient from "../../../utilities/apiClient";
import {GenerateErrorDisplayElement} from "../../../utilities/Error";
import { TranslationComponent, TranslationInterpreterComponent } from "../components";
import fetchProtectedFile from "../../../utilities/fetchProtectedFile";
interface Translation {
    id: number;
    customer: {id:number, first_name:string, last_name:string};
    interpreter: {id:number, first_name:string, last_name:string};
    language: {id:number, language_name:string};
    word_count: number;
    company: string;
    invoice_generated: boolean;
    document: string;
  }

interface Interpreter {
    id: number;
    first_name: string;
    last_name: string;
    email: string;
    phone_number: string;
    gender: string;
    offered_appointments: number[];
    offered_translations: number[];
}

function TranslationsMatchingPage() {

    const [translations, setTranslations] = useState<Translation[] | null>(null);
    const [interpreters, setInterpreters] = useState<Interpreter[] | null>(null);
    const [errorElm, setErrorElm] = useState(<div></div>);
    const [selectedTranslation, setSelectedTranslation] = useState<Translation | null>(null);
    
    const fetchTranslations = () => {
        apiClient.post("/fetch-translations/", {"unassigned" : true})
            .then((res) => {
                if (res.data.status == "success") {
                    console.log("Translations response:", res.data.result);
                    setTranslations(res.data.result);
                    console.log(res.data.result)
                } else if (res.data.status == "error") {
                    setErrorElm(GenerateErrorDisplayElement(res.data.error));
                }
            })
            .catch((err) => {
                setErrorElm(GenerateErrorDisplayElement(err.response?.data.error));
            });
    };

    const fetchInterpreters = () => {
        apiClient.get("/all-interpreters/")
            .then((res) => {
                if (res.data.status == "success") {
                    setInterpreters(res.data.result);
                    console.log(res.data.result)
                } else if (res.data.status == "error") {
                    setErrorElm(GenerateErrorDisplayElement(res.data.error));
                }
            })
            .catch((err) => {
                setErrorElm(GenerateErrorDisplayElement(err.response?.data.error));
            });
    };

    const updateInterpreterTranslationOffering = (translationID:number, interpreterOfferings:number[], interpreterID:number) => {
        const returnData = {
            translationID: translationID,
            interpreterID: interpreterID,
            offer: !interpreterOfferings.includes(translationID),
        }
        apiClient.post("/offer-translations/", returnData)
        .then((res) => {
            if (res.data.status == "success") {
                console.log("Offering Successful:", res.data);
                fetchInterpreters();
            } else if (res.data.status == "error") {
                setErrorElm(GenerateErrorDisplayElement(res.data.error));
            }
        })
        .catch((err) => {
            setErrorElm(GenerateErrorDisplayElement(err.response?.data.error));
        });
    }

    useEffect(() => {
        fetchTranslations();
        fetchInterpreters();
        const refreshRequests = setInterval(fetchTranslations, 15000);
        return () => clearInterval(refreshRequests);
    }, []);


    let filename: string = selectedTranslation?.document.replace("/media/translation_documents/", "")|| "";
    
    return (
        <>
        <div className="main-container container">
            <main className="main-content">
                <div>
                    <h3>Translation Matching</h3>
                </div>

                {errorElm}

                { selectedTranslation ? (
                    <>
                    <div className="d-lg-flex flex-wrap">
                        <div className="mb-3 col-lg-3">
                            <h4 className="my-3">Selected Translation:</h4>
                            <div className="card row-xs">
                                <ul className="list-group list-group-flush">
                                    <li className="list-group-item"><strong>Customer:</strong> {selectedTranslation.customer.first_name} {selectedTranslation.customer.last_name}</li>
                                    <li className="list-group-item"><strong>Language:</strong> {selectedTranslation.language.language_name}</li>
                                    <li className="list-group-item"><strong>Word Count:</strong> {selectedTranslation.word_count}</li>
                                    <li className="list-group-item"><strong>Company:</strong> {selectedTranslation.company}</li>
                                    <li className="list-group-item"><strong>Document:</strong> <button className="btn btn-link p-0" onClick={() => fetchProtectedFile(filename)}><i className="bi bi-download me-2"></i>{filename}</button></li>
                                </ul>
                                <div className="card-footer">
                                    <button className="btn btn-primary" onClick={() => setSelectedTranslation(null)}>Select a different Translation</button>
                                </div>
                            </div>
                        </div>

                        <div className="col ms-lg-3">
                            <h4 className="my-3">Offer to Interpreters:</h4>
                            <div className="px-3 pt-2 border-start bg-body-tertiary mt-3">
                                <p className="pb-2">
                                    Select an interpreter to offer them the selected translation. <br/>
                                    Or re-select an interpreter to un-offer them the selected translation.
                                </p>
                            </div>
                            <div className="d-flex flex-wrap">
                                {interpreters?.map((int, index) => (
                                    <div className="m-2" key={index} onClick={() => updateInterpreterTranslationOffering(selectedTranslation.id, int.offered_translations, int.id)}>
                                        <TranslationInterpreterComponent selectedTranslation={selectedTranslation} interpreter={int} />
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                    </>
                ) : (

                    <section className="d-md-flex pt-3">
                        <div className="col">
                            <h4>Select an Translation to match with an Interpreter:</h4>
                            <div className="d-flex flex-wrap">
                                {translations?.map((translation, index) => (
                                    <div className="m-2" key={index} onClick={() => setSelectedTranslation(translation)}>
                                        <TranslationComponent translation={translation} />
                                    </div>
                                ))}
                            </div>
                        </div>
                        <div className="col-md-4">
                            <div className="px-3 pt-2 ms-4 border-start bg-body-tertiary mt-3 pb-2">
                                Make sure to offer translations to interpreters who can translate the 
                                corresponding language.
                            </div>
                        </div>
                    </section>
                
                )}
            </main>
        </div>
        </>
    );    
}

export default TranslationsMatchingPage;