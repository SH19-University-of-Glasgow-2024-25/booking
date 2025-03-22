import React, { useEffect, useState } from "react";
import apiClient from "../../../utilities/apiClient";
import { GenerateErrorDisplayElement } from "../../../utilities/Error";
import { AppointmentComponent } from "../components";
import Toast from 'react-bootstrap/Toast';
import ToastContainer from 'react-bootstrap/ToastContainer';

interface Appointment {
    id: number;
    location: string;
    planned_start_time: string;
    planned_duration: string;
    customer: {id:number, first_name:string, last_name:string};
    interpreter: {id:number, first_name:string, last_name:string};
    language: {id:number, language_name:string};
    gender_preference: string;
    company: string;
    invoice_generated: boolean;
  }

function JobOverview() {
    const [appointments, setAppointments] = useState<Appointment[] | null>(null);
    const [errorElm, setErrorElm] = useState(<div></div>);
    const [outstandingFilter, setOutstandingFilter] = useState<true | false | null>(true);
    const [showInvoiceToast, setShowInvoiceToast] = useState(false);
    const [showUninvoiceToast, setShowUninvoiceToast] = useState(false);

    const handleOutstandingFilter = (e: React.ChangeEvent<HTMLSelectElement>) => {
        const value = e.target.value;
        setOutstandingFilter(value === "true" ? true : value === "false" ? false : null);
    }

    const fetchAppointments = () => {
        apiClient.post("/fetch-appointments/", {"unassigned" : false})
            .then((res) => {
                if (res.data.status == "success") {
                    setAppointments(res.data.result);
                    console.log(res.data.result)
                } else if (res.data.status == "error") {
                    setErrorElm(GenerateErrorDisplayElement(res.data.error));
                }
            })
            .catch((err) => {
                setErrorElm(GenerateErrorDisplayElement(err.response?.data.error));
            });
    };

    const toggleInvoice = (appointmentID:number, invoice_generated: boolean) => {
        apiClient.post("/toggle-appointment-invoice/", {appID: appointmentID})
        .then((res) => {
            if (res.data.status == "success") {
                console.log("Toggle Successful:", res.data);
                if (!invoice_generated && outstandingFilter === true)
                    setShowInvoiceToast(true);
                if (invoice_generated && outstandingFilter === false)
                    setShowUninvoiceToast(true);
                fetchAppointments();
            } else if (res.data.status == "error") {
                setErrorElm(GenerateErrorDisplayElement(res.data.error));
            }
        })
        .catch((err) => {
            setErrorElm(GenerateErrorDisplayElement(err.response?.data.error));
        });
    }

    useEffect(() => {
            fetchAppointments();
            const refreshRequests = setInterval(fetchAppointments, 15000);
            return () => clearInterval(refreshRequests);
        }, []);

    return <>
        <div className="container d-md-flex pt-3">
            <div className="col">
                <main className="main-content">
                    <div>
                        <h3>Assigned Appointments Overview</h3>
                        <select className="form-select mb-3" onChange={handleOutstandingFilter} value={String(outstandingFilter)}>
                            <option value="null">All Appointments</option>
                            <option value="true">Outstanding</option>
                            <option value="false">Invoice Generated</option>
                        </select>
                    </div>
                    <hr/>
                    {errorElm}
                    <div className="px-3 pt-2 border-start bg-body-tertiary mt-3 pb-2 mb-2">
                        Select an appointment to generate an invoice. <br/>
                        Or re-select an appointment to remove an invoice.
                    </div>
                    <div className="d-flex flex-wrap">
                        {appointments
                            ?.filter(app => outstandingFilter !== app.invoice_generated)
                            .map((app, index) => (
                                <div className="m-2" key={index} onClick={() => toggleInvoice(app.id, app.invoice_generated)}>
                                    <AppointmentComponent appointment={app} />
                                </div>
                            ))
                        }
                    </div>
                </main>
            </div>
            <div className="col-md-3">
                <div className="px-3 pt-2 ms-4 border-start bg-body-tertiary mt-3 pb-2">
                    After selecting an appointment to invoice, 
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
                        The appointment has been moved to the &quot;Invoice Generated&quot; tab.
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
                        The appointment has been moved to the &quot;Outstanding&quot; tab.
                    </span>
                </Toast.Body>
            </Toast>
        </ToastContainer>
    </>;
}

export default JobOverview;