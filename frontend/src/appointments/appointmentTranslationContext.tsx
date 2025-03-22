import { createContext } from 'react';

interface AppointmentTranslationContextType {
    appointmentOrTranslation: "Appointments" | "Translations";
    setAppointmentOrTranslation: (type: "Appointments" | "Translations") => void;
}

const AppointmentTranslationContext = createContext<AppointmentTranslationContextType>({
    appointmentOrTranslation: "Appointments",
    setAppointmentOrTranslation: () => {},
});

export default AppointmentTranslationContext;
