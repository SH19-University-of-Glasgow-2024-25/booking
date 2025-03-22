import { useContext } from "react";
import AppointmentTranslationContext from "../appointments/appointmentTranslationContext";
import { useNavigate, useLocation } from 'react-router-dom';

export function InterpreterJobNavbar() {
    const { appointmentOrTranslation, setAppointmentOrTranslation } = useContext(AppointmentTranslationContext);
    const navigate = useNavigate();
    const currentPath = useLocation().pathname;

    return (<div className="navbar navbar-expand-lg bg-body-tertiary green-texture" data-bs-theme="dark">
        <div className="container">
            <div className="navbar-brand text-light">
                Appointments and Translations
            </div>
            <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbar-collapse-2">
                <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbar-collapse-2">
                <ul className="navbar-nav ms-auto mb-2 mb-lg-0">
                    <li className="list-item">
                        <button className="btn btn-link link-light link-underline-light link-offset-2 link-underline-opacity-75" 
                                onClick={() => navigate("/" + appointmentOrTranslation.toLowerCase())}>
                                    {appointmentOrTranslation.substring(0, appointmentOrTranslation.length - 1)} Offers
                                </button>
                    </li>
                    
                    <li className="list-item">
                        <button className="btn btn-link link-light link-underline-light link-offset-2 link-underline-opacity-75" 
                                 onClick={() => navigate("/" + appointmentOrTranslation.toLowerCase() + "/accepted")}>
                                    Upcoming {appointmentOrTranslation}
                                </button>
                    </li>
                </ul>
                <select
                    value={appointmentOrTranslation} 
                    onChange={(e) => {
                        setAppointmentOrTranslation(e.target.value as "Appointments" | "Translations");

                        let isStateChange = !currentPath.includes(e.target.value.toLowerCase());
                        if (isStateChange) {
                            console.log("state change");
                            if (currentPath.includes("/appointments"))
                                navigate(currentPath.replace("/appointments", "/translations"));
                            else if (currentPath.includes("/translations"))
                                navigate(currentPath.replace("/translations", "/appointments"));
                        }
                    }}
                    >
                    <option value="Appointments">Appointments</option>
                    <option value="Translations">Translations</option>
                </select>
            </div>
        </div>
    </div>
    );
}