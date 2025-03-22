import { useEffect, useState } from "react";
import apiClient from "../../../utilities/apiClient";
import {GenerateErrorDisplayElement} from "../../../utilities/Error";
import { AppointmentComponent, AppointmentInterpreterComponent} from "../components";

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

function AppointmentsMatchingPage() {

    const [appointments, setAppointments] = useState<Appointment[] | null>(null);
    const [interpreters, setInterpreters] = useState<Interpreter[] | null>(null);
    const [errorElm, setErrorElm] = useState(<div></div>);
    const [selectedAppointment, setSelectedAppointment] = useState<Appointment | null>(null);
    
    const fetchAppointments = () => {
        apiClient.post("/fetch-appointments/", {"unassigned" : true})
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

    const updateInterpreterAppointmentOffering = (appointmentID:number, interpreterOfferings:number[], interpreterID:number) => {
        const returnData = {
            appID: appointmentID,
            interpreterID: interpreterID,
            offer: !interpreterOfferings.includes(appointmentID),
        }
        apiClient.post("/offer-appointments/", returnData)
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
        fetchAppointments();
        fetchInterpreters();
        const refreshRequests = setInterval(fetchAppointments, 15000);
        return () => clearInterval(refreshRequests);
    }, []);

    return (
        <>
        <div className="main-container container">
            <main className="main-content">
                <div>
                    <h3>Appointment Matching</h3>
                </div>

                {errorElm}

                { selectedAppointment ? (
                    <>
                    <div className="d-lg-flex flex-wrap">
                        <div className="mb-3 col-lg-3">
                            <h4 className="my-3">Selected Appointment:</h4>
                            <div className="card row-xs">
                                <ul className="list-group list-group-flush">
                                    <li className="list-group-item"><strong>Location:</strong> {selectedAppointment.location}</li>
                                    <li className="list-group-item"><strong>Start Time:</strong> {selectedAppointment.planned_start_time}</li>
                                    <li className="list-group-item"><strong>Duration:</strong> {selectedAppointment.planned_duration}</li>
                                    <li className="list-group-item"><strong>Customer:</strong> {selectedAppointment.customer.first_name} {selectedAppointment.customer.last_name}</li>
                                    <li className="list-group-item"><strong>Language:</strong> {selectedAppointment.language.language_name}</li>
                                    <li className="list-group-item"><strong>Gender Preference:</strong> {selectedAppointment.gender_preference}</li>
                                    <li className="list-group-item"><strong>Company:</strong> {selectedAppointment.company}</li>
                                </ul>
                                <div className="card-footer">
                                    <button className="btn btn-primary" onClick={() => setSelectedAppointment(null)}>Select a different Appointment</button>
                                </div>
                            </div>
                        </div>

                        <div className="col ms-lg-3">
                            <h4 className="my-3">Offer to Interpreters:</h4>
                            <div className="px-3 pt-2 border-start bg-body-tertiary mt-3">
                                <p className="pb-2">
                                    Select an interpreter to offer them the selected appointment. <br/>
                                    Or re-select an interpreter to un-offer them the selected appointment.
                                </p>
                            </div>
                            <div className="d-flex flex-wrap">
                                {interpreters?.map((int, index) => (
                                    <div className="m-2" key={index} onClick={() => updateInterpreterAppointmentOffering(selectedAppointment.id, int.offered_appointments, int.id)}>
                                        <AppointmentInterpreterComponent selectedAppointment={selectedAppointment} interpreter={int} />
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                    </>
                ) : (

                    <section className="d-md-flex pt-3">
                        <div className="col">
                            <h4>Select an Appointment to match with an Interpreter:</h4>
                            <div className="d-flex flex-wrap">
                                { appointments?.length != 0 ? appointments?.map((app, index) => (
                                    <div className="m-2" key={index} onClick={() => setSelectedAppointment(app)}>
                                        <AppointmentComponent appointment={app} />
                                    </div>
                                )) : (
                                    <p>No unaccepted appointments!</p>
                                )}
                            </div>
                        </div>
                        <div className="col-md-4">
                            <div className="px-3 pt-2 ms-4 border-start bg-body-tertiary mt-3 pb-2">
                                The actual duration of an appointment may vary from the planned duration,
                                this should be updated by interpreters.
                            </div>
                        </div>
                    </section>
                
                )}
            </main>
        </div>
        </>
    );    
}

export default AppointmentsMatchingPage;