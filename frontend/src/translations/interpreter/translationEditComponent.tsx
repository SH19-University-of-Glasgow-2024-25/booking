import { useState } from "react";
import apiClient from "../../utilities/apiClient";
import {GenerateErrorDisplayElement} from "../../utilities/Error";
import fetchProtectedFile from "../../utilities/fetchProtectedFile";

interface Translation {
    id: number;
    customer: {id:number, first_name:string, last_name:string};
    language: {id:number, language_name:string};
    word_count: number;
    company: string;
    document: string;
    actual_word_count?: number;
}

export default function EditTranslationComponent({
        translation,
        fetchTranslations,
	setErrorElm
    }: {
        translation: Translation;
        fetchTranslations: () => void;
	setErrorElm: (errorGenerator: JSX.Element) => void;
    }) {
        const [editMode, setEditMode] = useState<boolean>(false);
        const [actualWordCount, setActualWordCount] = useState<number | null>(
			translation.actual_word_count ? translation.actual_word_count : null
		);

        const updateTranslation = () => {
            const requestData = {
                translationID : translation.id,
                actualWordCount : actualWordCount
            }
            apiClient.post("/set-translations-actual-word-count/", requestData)
                .then((res) => {
                        if (res.data.status == "success") {
                                fetchTranslations();
								setErrorElm(<div/>);
                        } else if (res.data.status == "error") {
                                setErrorElm(GenerateErrorDisplayElement(res.data.error));
                        }
                })
                .catch((err) => {
                        setErrorElm(GenerateErrorDisplayElement(err.response?.data.error));
                });
        }

        let filename: string = translation.document.replace("/media/translation_documents/", ""); 

        return (
            <>
                <div className="card row-xs">
                    <ul className="list-group list-group-flush">
                        <li className="list-group-item">
                        <div className="d-flex justify-content-between align-items-center">
                            <div>
                            Customer: <h5 className="card-title">{translation.customer.first_name} {translation.customer.last_name}</h5>
                            </div>
                            {editMode ? 
                            <div>
                                <button onClick={() => {updateTranslation(); setEditMode(false);}} className="btn btn-lg p-0 btn-link link-success me-2">
                                <i className="bi bi-check-circle"></i>
                                </button>
                                <button onClick={() => {setEditMode(false);}} className="btn btn-lg p-0 btn-link link-danger">
                                <i className="bi bi-x-circle"></i>
                                </button>
                            </div>
                            :
                            <div>
                                <button
                                className="btn btn-primary"
                                onClick={() => setEditMode(true)}
                                >
                                <i className="bi bi-pencil-fill"></i> Edit
                                </button>
                            </div>
                            }
                        </div>
                        </li>
                        <li className="list-group-item">Language: {translation.language.language_name}</li>
                        <li className="list-group-item">Word count: {translation.word_count}</li>
                        <li className="list-group-item">Company: {translation.company}</li>
                        <li className="list-group-item">
                            Actual word count:&nbsp;
                            {editMode ? 
                                <input
                                    className="form-control"
                                    type="number"
                                    value={actualWordCount ? actualWordCount : ""}
                                    onChange={(e) => setActualWordCount(
                                        e.target.value === "" ? null : parseInt(e.target.value)
                                    )}
                                />
                                :
                                <>{translation.actual_word_count ? translation.actual_word_count : <>Unset</>}</>
                            }
                        </li>
                        <li className="list-group-item"><strong>Document:</strong> <button className="btn btn-link p-0" onClick={() => fetchProtectedFile(filename)}><i className="bi bi-download me-2"></i>{filename}</button></li>
                    </ul>
                </div>           
            </>
        );        
}