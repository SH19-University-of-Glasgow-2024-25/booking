import { useContext, useEffect, useState } from "react";
import apiClient from "../../utilities/apiClient";
import {GenerateErrorDisplayElement} from "../../utilities/Error";
import EditTranslationComponent from "./translationEditComponent";
import { InterpreterJobNavbar } from "../../utilities/interpreterJobNavbar";
import AppointmentTranslationContext from "../../appointments/appointmentTranslationContext";

interface Translation {
    id: number;
    customer: {id:number, first_name:string, last_name:string};
    language: {id:number, language_name:string};
    word_count: number;
    document: string;
    company: string;
    actual_word_count?: number;
}

function TranslationManagementPage() {
    const [translations, setTranslations] = useState<Translation[] | null>(null);
    const [errorElm, setErrorElm] = useState(<div></div>);

    const { setAppointmentOrTranslation } = useContext(AppointmentTranslationContext);
    useEffect(() => setAppointmentOrTranslation("Translations"));
    
    const fetchTranslations = () => {
        apiClient.post("/fetch-accepted-translations/")
            .then((res) => {
                if (res.data.status == "success") {
                    setTranslations(res.data.result)
                    console.log(res.data.result);
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
    }, []);

    return (
        <>
        <InterpreterJobNavbar/>
        <div className="container d-md-flex pt-3">
            <div className="col">
                <main className="main-content">
                    <div>
                        <h3>Upcoming Translations:</h3>
                    </div>

                    {errorElm}
                    
                    <div className="d-flex flex-wrap">
                        {translations && translations.length != 0 ? translations?.map((translation) => (
                            <div key={translation.id} className="m-2">
                                <EditTranslationComponent
                                    translation={translation}
                                    fetchTranslations={fetchTranslations}
                                    setErrorElm={setErrorElm}
                                />
                            </div>
                        )) : (
                            <p>No accepted translations!</p>
                        )}
                    </div>
                </main>
            </div>

            <div className="col-md-3">
                <div className="px-3 pt-2 ms-4 border-start bg-body-tertiary mt-3 pb-2 border-warning">
                    <h5>Remember...</h5>
                    Update the &quot;Actual word count&quot; after each translation, so that customers
                    can be billed correctly.
                </div>
            </div>
        </div>
        </>
    );    
}

export default TranslationManagementPage;