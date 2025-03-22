import ProtectedContent from '../utilities/ProtectedContent';
import AppointmentsAcceptancePage from "./interpreter/appointmentAcceptance";
import AppointmentsCreationPage from "./customer/appointmentsCreation";
import AppointmentsManagementPage from "./admin/adminAppointment.tsx";
import AppointmentTranslationContext from './appointmentTranslationContext.tsx';
import { useState } from 'react';

function AppointmentsPage() {
    const [appointmentOrTranslation, setAppointmentOrTranslation] = useState<"Appointments" | "Translations">("Appointments");

    return (
        <AppointmentTranslationContext.Provider value={{ appointmentOrTranslation, setAppointmentOrTranslation }}>
            <ProtectedContent admin_access>
                <AppointmentsManagementPage/>
            </ProtectedContent>
            <ProtectedContent interpreter_access>
                <AppointmentsAcceptancePage/>
            </ProtectedContent>
            <ProtectedContent customer_access>
                <div className="navbar green-texture" data-bs-theme="dark">
                    <div className="container">
                        <div className="navbar-inner">
                            <div className="navbar-brand">
                                Appointments
                            </div>
                        </div>
                    </div>
                </div>
                <AppointmentsCreationPage/>
            </ProtectedContent>
        </AppointmentTranslationContext.Provider>
    );    
}

export default AppointmentsPage;