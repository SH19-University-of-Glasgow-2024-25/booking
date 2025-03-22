import { useContext, useState } from "react";
import AppointmentsMatchingPage from "./appointments/appointmentsMatching";
import AppointmentsOverview from "./appointments/appointmentsOverview";
import AppointmentTranslationContext from "../appointmentTranslationContext";
import TranslationsMatchingPage from "./translations/translationsMatching";
import TranslationsOverview from "./translations/translationsOverview";

function AdminAppointment() {
    const [tab, setTab] = useState<"manage" | "match">("manage");
    const { appointmentOrTranslation, setAppointmentOrTranslation } = useContext(AppointmentTranslationContext);

    console.log(appointmentOrTranslation)

    return (
        <>
            <div className="navbar navbar-expand-lg bg-body-tertiary green-texture" data-bs-theme="dark">
                <div className="container">
                    <div className="navbar-brand text-light">
                        Job Management
                    </div>
                    <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbar-collapse-2">
                        <span className="navbar-toggler-icon"></span>
                    </button>
                    <div className="collapse navbar-collapse" id="navbar-collapse-2">
                        <ul className="navbar-nav ms-auto mb-2 mb-lg-0">
                            <li className="list-item">
                                <button className="btn btn-link link-light link-underline-light link-offset-2 link-underline-opacity-75" onClick={() => setTab("manage")}>Overview</button>
                            </li>
                            
                            <li className="list-item">
                                <button className="btn btn-link link-light link-underline-light link-offset-2 link-underline-opacity-75" onClick={() => setTab("match")}>Match {appointmentOrTranslation}</button>
                            </li>
                        </ul>
                        <select
                            value={appointmentOrTranslation} 
                            onChange={(e) => setAppointmentOrTranslation(e.target.value as "Appointments" | "Translations")}
                            >
                            <option value="Appointments">Appointments</option>
                            <option value="Translations">Translations</option>
                        </select>
                    </div>
                </div>
            </div>
            {tab === "manage" && appointmentOrTranslation === "Appointments" && <AppointmentsOverview />}
            {tab === "match" && appointmentOrTranslation === "Appointments" && <AppointmentsMatchingPage />}
            {tab === "manage" && appointmentOrTranslation === "Translations" && <TranslationsOverview />}
            {tab === "match" && appointmentOrTranslation === "Translations" && <TranslationsMatchingPage />}
        </>
    );
}

export default AdminAppointment;