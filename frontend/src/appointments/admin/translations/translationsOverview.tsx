import React, { useEffect, useState } from "react";
import apiClient from "../../../utilities/apiClient";
import { GenerateErrorDisplayElement } from "../../../utilities/Error";
import { TranslationComponent } from "../components";
import Toast from 'react-bootstrap/Toast';
import ToastContainer from 'react-bootstrap/ToastContainer';

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

function JobOverview() {
    const [translations, setTranslations] = useState<Translation[] | null>(null);
    const [errorElm, setErrorElm] = useState(<div></div>);
    const [outstandingFilter, setOutstandingFilter] = useState<true | false | null>(true);
    const [showInvoiceToast, setShowInvoiceToast] = useState(false);
    const [showUninvoiceToast, setShowUninvoiceToast] = useState(false);

    const handleOutstandingFilter = (e: React.ChangeEvent<HTMLSelectElement>) => {
        const value = e.target.value;
        setOutstandingFilter(value === "true" ? true : value === "false" ? false : null);
    }

    const fetchTranslations = () => {
        apiClient.post("/fetch-translations/", {"unassigned" : false})
            .then((res) => {
                if (res.data.status == "success") {
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

    const toggleInvoice = (translationID:number, invoice_generated: boolean) => {
        apiClient.post("/toggle-translation-invoice/", {translationID: translationID})
        .then((res) => {
            if (res.data.status == "success") {
                console.log("Toggle Successful:", res.data);
                if (!invoice_generated && outstandingFilter === true)
                    setShowInvoiceToast(true);
                if (invoice_generated && outstandingFilter === false)
                    setShowUninvoiceToast(true);
                fetchTranslations();
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
            const refreshRequests = setInterval(fetchTranslations, 15000);
            return () => clearInterval(refreshRequests);
        }, []);

    return <>
        <div className="container d-md-flex pt-3">
            <div className="col">
                <main className="main-content">
                    <div>
                        <h3>Assigned Translations Overview</h3>
                        <select className="form-select mb-3" onChange={handleOutstandingFilter} value={String(outstandingFilter)}>
                            <option value="null">All Translations</option>
                            <option value="true">Outstanding</option>
                            <option value="false">Invoice Generated</option>
                        </select>
                    </div>
                    <hr/>
                    {errorElm}
                    <div className="px-3 pt-2 border-start bg-body-tertiary mt-3 pb-2 mb-2">
                        Select a translation to generate an invoice. <br/>
                        Or re-select a translation to remove an invoice.
                    </div>
                    <div className="d-flex flex-wrap">
                        {translations
                            ?.filter(translation => outstandingFilter !== translation.invoice_generated)
                            .map((translation, index) => (
                                <div className="m-2" key={index} onClick={() => toggleInvoice(translation.id, translation.invoice_generated)}>
                                    <TranslationComponent translation={translation} />
                                </div>
                            ))
                        }
                    </div>
                </main>
            </div>
            <div className="col-md-3">
                <div className="px-3 pt-2 ms-4 border-start bg-body-tertiary mt-3 pb-2">
                    After selecting a translation to invoice, 
                    it will be accessible in the &quot;Invoice Generated&quot; tab.
                </div>
            </div>
        </div>

        <ToastContainer position="bottom-center" className="p-3" style={{ zIndex: 1 }}>
            <Toast onClose={() => setShowInvoiceToast(false)} show={showInvoiceToast} delay={6000} autohide className="bg-dark">
                <Toast.Body>
                    <span className="text-success">
                        An invoice has been successfully generated! 
                    </span>

                    <br/>
                    
                    <span className="text-light">
                        The translation has been moved to the &quot;Invoice Generated&quot; tab.
                    </span>
                </Toast.Body>
            </Toast>

            <Toast onClose={() => setShowUninvoiceToast(false)} show={showUninvoiceToast} delay={6000} autohide className="bg-dark">
                <Toast.Body>
                    <span className="text-success">
                        Invoice has been removed.
                    </span>

                    <br/>
                    
                    <span className="text-light">
                        The translation has been moved to the &quot;Outstanding&quot; tab.
                    </span>
                </Toast.Body>
            </Toast>
        </ToastContainer>
    </>;
}

export default JobOverview;