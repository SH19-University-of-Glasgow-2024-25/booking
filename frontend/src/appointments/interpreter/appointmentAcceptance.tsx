import { useEffect, useState } from "react";
import apiClient from "../../utilities/apiClient";
import {GenerateErrorDisplayElement} from "../../utilities/Error";
import { OfferComponent } from "./offerComponent";
import { InterpreterJobNavbar } from "../../utilities/interpreterJobNavbar";

import { useContext } from "react";
import AppointmentTranslationContext from "../appointmentTranslationContext";
import { Toast, ToastContainer } from "react-bootstrap";

interface Appointment {
    id: number;
    location: string;
    planned_start_time: string;
    planned_duration: string;
    customer: {id:number, first_name:string, last_name:string};
    language: {id:number, language_name:string};
    gender_preference: string;
    company: string;
}

function AppointmentsAcceptancePage() {
    const [appointments, setAppointments] = useState<Appointment[] | null>(null);
    const [errorElm, setErrorElm] = useState(<div></div>);

    const [showAcceptToast, setShowAcceptToast] = useState(false);

    const { setAppointmentOrTranslation } = useContext(AppointmentTranslationContext);
    useEffect(() => setAppointmentOrTranslation("Appointments"));

    const fetchAppointments = () => {
        apiClient.post("/offered-appointments/")
            .then((res) => {
                if (res.data.status == "success") {
                    setAppointments(res.data.result);
                    console.log(res.data.result);
                } else if (res.data.status == "error") {
                    setErrorElm(GenerateErrorDisplayElement(res.data.error));
                }
            })
            .catch((err) => {
                setErrorElm(GenerateErrorDisplayElement(err.response?.data.error));
            });
    };

    const updateOfferringWithResponse = (appointmentID:number, accepted:boolean) => {
        const returnData = {
            appID: appointmentID,
            accepted: accepted,
        }
        apiClient.post("/updated-appointments/", returnData)
        .then((res) => {
            console.log(res.data)
            if (res.data.status == "success") {
                console.log("Offering Successful:", res.data);
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

    return (
        <>
        <InterpreterJobNavbar/>
        <div className="container d-md-flex pt-3">
            <div className="col">
                <main className="main-content">
                    <div>
                        <h3>Appointment offers:</h3>
                    </div>

                    {errorElm}

                    <div className="d-flex flex-wrap">
                        {appointments?.length != 0 ? appointments?.map((app) => (
                            <div key = {app.id} className="m-2">
                                <OfferComponent appointment={app} updateAppointment={updateOfferringWithResponse} setShowToast={setShowAcceptToast}/>
                            </div>
                        )) : (
                            <p>No appointment offers!</p>
                        )}
                    </div>
                </main>
            </div>

            <div className="col-md-3">
                <div className="px-3 pt-2 ms-4 border-start bg-body-tertiary mt-3 pb-2">
                    After accepting an appointment, it will move to the &quot;Upcoming Appointments&quot; tab.
                </div>
            </div>
        </div>

        <ToastContainer position="bottom-center" className="p-3" style={{ zIndex: 1 }}>
            <Toast onClose={() => setShowAcceptToast(false)} show={showAcceptToast} delay={6000} autohide className="bg-dark">
                <Toast.Body>
                    <span className="text-success">
                        You have accepted an appointment!
                    </span>

                    <br/>
                    
                    <span className="text-light">
                        The appointment has been moved to the &quot;Upcoming Appointments&quot; tab.
                    </span>
                </Toast.Body>
            </Toast>
        </ToastContainer>
        </>
    );    
}

export default AppointmentsAcceptancePage;