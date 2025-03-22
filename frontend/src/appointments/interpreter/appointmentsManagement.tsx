import { useContext, useEffect, useState } from "react";
import apiClient from "../../utilities/apiClient";
import {GenerateErrorDisplayElement} from "../../utilities/Error";
import EditAppointmentComponent from "./EditAppointmentComponent";
import { InterpreterJobNavbar } from "../../utilities/interpreterJobNavbar";
import AppointmentTranslationContext from "../appointmentTranslationContext";

interface Appointment {
    id: number;
    location: string;
    planned_start_time: string;
    planned_duration: string;
    customer: {id:number, first_name:string, last_name:string};
    language: {id:number, language_name:string};
    gender_preference: string;
    company: string;
    actual_start_time?: string;
    actual_duration?: string;
}

function AppointmentManagementPage() {
    const [appointments, setAppointments] = useState<Appointment[] | null>(null);
    const [errorElm, setErrorElm] = useState(<div></div>);

    const { setAppointmentOrTranslation } = useContext(AppointmentTranslationContext);
    useEffect(() => setAppointmentOrTranslation("Appointments"));
    
    const fetchAppointments = () => {
        apiClient.get("/accepted-appointments/")
            .then((res) => {
                if (res.data.status == "success") {
                    setAppointments(res.data.result.sort((a: Appointment, b: Appointment) => {
                        return new Date(a.planned_start_time).getTime() - new Date(b.planned_start_time).getTime();
                    }));
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
        fetchAppointments();
    }, []);

    return (
        <>
        <InterpreterJobNavbar/>
        <div className="container d-md-flex pt-3">
            <div className="col">
                <main className="main-content">
                    <div>
                        <h3>Upcoming Appointments:</h3>
                    </div>

                    {errorElm}
                    
                    <div className="d-flex flex-wrap">
                        {appointments?.length != 0 ? appointments?.map((app) => (
                            <div key={app.id} className="m-2">
                                <EditAppointmentComponent appointment={app} fetchAppointments={fetchAppointments}/>
                            </div>
                        )) : (
                            <p>No upcoming appointments!</p>
                        )}
                    </div>
                </main>
            </div>

            <div className="col-md-3">
                <div className="px-3 pt-2 ms-4 border-start bg-body-tertiary mt-3 pb-2 border-warning">
                    <h5>Remember...</h5>
                    Update the &quot;Actual Start&quot; and &quot;Actual Duration&quot; fields after each appointment, so that customers
                    can be billed correctly.
                </div>
            </div>
        </div>
        </>
    );    
}

export default AppointmentManagementPage;