import { useContext, useEffect, useState } from "react";
import apiClient from "../../utilities/apiClient";
import { GenerateErrorDisplayElement } from "../../utilities/Error";
import { TranslationOfferComponent } from "./translationOfferComponent";
import { InterpreterJobNavbar } from "../../utilities/interpreterJobNavbar";
import AppointmentTranslationContext from "../../appointments/appointmentTranslationContext";
import { Toast, ToastContainer } from "react-bootstrap";

interface Translation {
    id: number;
    customer: {id:number, first_name:string, last_name:string};
    language: {id:number, language_name:string};
    word_count: number;
    company: string;
    document: string;
}

function TranslationsAcceptancePage() {
    const [translations, setTranslations] = useState<Translation[] | null>(null);
    const [errorElm, setErrorElm] = useState(<div></div>);

    const [showAcceptToast, setShowAcceptToast] = useState(false);

    const { setAppointmentOrTranslation } = useContext(AppointmentTranslationContext);
    useEffect(() => setAppointmentOrTranslation("Translations"));

    const fetchTranslations = () => {
        apiClient.post("/offered-translations/")
            .then((res) => {
                if (res.data.status == "success") {
                    setTranslations(res.data.result);
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
        const refreshRequests = setInterval(fetchTranslations, 15000);
        return () => clearInterval(refreshRequests);
    }, []);

    const updateOfferring = (translationID:number, accepted:boolean) => {
        const returnData = {
            translationID: translationID,
            accepted: accepted,
        }
        apiClient.post("/update-translation/", returnData)
        .then((res) => {
            console.log(res.data)
            if (res.data.status == "success") {
                console.log("Offering Successful:", res.data);
                fetchTranslations();
                setErrorElm(<div></div>);
            } else if (res.data.status == "error") {
                setErrorElm(GenerateErrorDisplayElement(res.data.error));
            }
        })
        .catch((err) => {
            setErrorElm(GenerateErrorDisplayElement(err.response?.data.error));
        });
    }
    
    return (
        <>
        <InterpreterJobNavbar/>
        <div className="container d-md-flex pt-3">
            <div className="col">
                <main className="main-content">
                    <div>
                        <h3>Translation offers:</h3>
                    </div>

                    {errorElm}

                    <div className="d-flex flex-wrap">
                    {translations?.length != 0 ? translations?.map((translation) => (
                        <div key={translation.id} className="m-2">
                            <TranslationOfferComponent translation={translation} updateTranslation={updateOfferring} setShowToast={setShowAcceptToast}/>
                        </div>
                    )) : (
                        <p>No translation offers!</p>
                    )}
                </div>
                </main>
            </div>

            <div className="col-md-3">
                <div className="px-3 pt-2 ms-4 border-start bg-body-tertiary mt-3 pb-2">
                    After accepting a translation, it will move to the &quot;Upcoming Translations&quot; tab.
                </div>
            </div>
        </div>

        <ToastContainer position="bottom-center" className="p-3" style={{ zIndex: 1 }}>
            <Toast onClose={() => setShowAcceptToast(false)} show={showAcceptToast} delay={6000} autohide className="bg-dark">
                <Toast.Body>
                    <span className="text-success">
                        You have accepted a translation!
                    </span>

                    <br/>
                    
                    <span className="text-light">
                        The translation has been moved to the &quot;Upcoming Translations&quot; tab.
                    </span>
                </Toast.Body>
            </Toast>
        </ToastContainer>
        </>
    );    
}

export default TranslationsAcceptancePage;