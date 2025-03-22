import React, { useState, useEffect } from "react";
import apiClient from "../../utilities/apiClient";
import Select from "react-select";
import {GenerateErrorDisplayElement} from "../../utilities/Error";

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
function AppointmentsCreationPage() {

    const [planned_start_time, setPlannedStartTime] = useState('');
    const [planned_duration,  setPlannedDuration] = useState('01:00');
    const [location,  setLocation] = useState('');
    const [company, setCompany] = useState('');
    const [gender, setGender] = useState('');
    const [language, setLanguage] = useState<{ value: string; label: string} | null>(null);
    const [notes, setNotes] = useState('')
    const [languageOptions, setLanguageOptions] = useState([]);
    const [errorElm, setErrorElm] = useState(<div></div>);
    const [appointments, setAppointments] = useState<Appointment[] | null>(null);

    const clearForm = () => {
        setPlannedStartTime('');
        setPlannedDuration('');
        setLocation('');
        setGender('');
        setLanguage(null);
        setNotes('');
    }
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
    const fetchAppointments = () => {
        apiClient.get("/appointments/")
            .then((res) => {
                console.log(res.data.result.result)
                if (res.data.status == "success") {
                    setAppointments(res.data.result.result)
                } else if (res.data.status == "error") {
                    setErrorElm(GenerateErrorDisplayElement(res.data.error));
                }
            })
            .catch((err) => {
                setErrorElm(GenerateErrorDisplayElement(err.response?.data.error));
            });
    };

    useEffect(() => {
        fetchData();
        fetchAppointments();
    }, []);

    const submitAppointmentCreation = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        console.log("Submitting appointment form")
        if (!language) {
            console.error("No language selected.");
            return;
        }
        console.log(language.value)
        const returnData = {
            planned_start_time: planned_start_time,
            planned_duration: planned_duration,
            location: location,
            company: company,
            gender: gender,
            language: language.value,
            notes: notes,
        }
        apiClient.post("/appointment-request/", returnData)
            .then((res) => {
                console.log("Appointment Creation Successful:", res.data);
                clearForm();
                fetchAppointments();
            })
            .catch((err) => {
            console.error("Appointment Creation Error Response:", err.response?.data);
        });
    }

    return (
        <>
            <div className="main-container container">
                <div className="d-flex">
                    <div className="col-4">
                        <h4>Request a New Appointment</h4>
                        <form className="form" onSubmit={submitAppointmentCreation}>
                            <div className="mb-2">
                                <label className="form-label">Planned Start Time:</label>
                                <input
                                    className="form-control"
                                    type="datetime-local"
                                    value={planned_start_time}
                                    onChange={(e) => setPlannedStartTime(e.target.value)}
                                    required
                                />
                            </div>

                            <div className="mb-2">
                                <label className="form-label">Planned Duration:</label>
                                <input
                                    className="form-control"
                                    type="time"
                                    value={planned_duration}
                                    onChange={(e) => setPlannedDuration(e.target.value)}
                                    required
                                />
                            </div>

                            <div className="mb-2">
                                <label className="form-label">Location:</label>
                                <input
                                    className="form-control"
                                    type="text"
                                    value={location}
                                    onChange={(e) => setLocation(e.target.value)}
                                    required
                                />
                            </div>

                            <div className="mb-2">
                                <label className="form-label">Language</label>
                                <Select
                                    options={languageOptions}
                                    value={language}
                                    onChange={(selectedOption) => setLanguage(selectedOption)}
                                    placeholder="Select a language..."
                                    required
                                />
                            </div>

                            <div className="mb-2">
                                <label className="form-label">Gender Preference:</label>
                                <select className="form-select" value={gender} onChange={(e) => setGender(e.target.value)} required>
                                    <option value="">Select Gender</option>
                                    <option value="M">Male</option>
                                    <option value="F">Female</option>
                                    <option value="O">Other</option>
                                    <option value="X">No Preference</option>
                                </select>
                            </div>

                            <div className="mb-2">
                                <label className="form-label">Company</label>
                                <input
                                    className="form-control"
                                    type="text"
                                    value={company}
                                    onChange={(e) => setCompany(e.target.value)}
                                />
                            </div>

                            <div className="mb-3">
                                <label className="form-label">Notes/Description:</label>
                                <textarea className="form-control" value={notes} onChange={(e) => setNotes(e.target.value)} />
                            </div>

                            <button className="btn btn-primary" type="submit">Request Appointment</button>
                            {errorElm}
                        </form>
                    </div>

                    <div className="col ms-3">
                        <h4>Your Appointments</h4>
                        <div className="d-flex">
                        {appointments &&
                            appointments.map((appointment, index) => (
                                <div key={index} className="card row-xs m-1">
                                    <ul className="list-group list-group-flush">
                                    <li className="list-group-item">Customer: <h5 className="card-title">{appointment.customer.first_name} {appointment.customer.last_name}</h5></li>
                                    <li className="list-group-item">Language: {appointment.language.language_name}</li>
                                    <li className="list-group-item">When: {appointment.planned_start_time}</li>
                                    <li className="list-group-item">Duration: {appointment.planned_duration}</li>
                                    <li className="list-group-item">Where: {appointment.location}</li>
                                    <li className="list-group-item">Gender Preference: {appointment.gender_preference}</li>
                                    <li className="list-group-item">Company: {appointment.company}</li>
                                    </ul>
                                </div>
                            ))}
                        {(appointments && appointments?.length == 0) && <p>No appointments requested!</p>}
                        </div>
                    </div>
                </div>
            </div>
        </>
    );  
}

export default AppointmentsCreationPage;