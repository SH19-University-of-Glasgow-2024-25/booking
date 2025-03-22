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

export function AppointmentComponent({
    appointment,
  }: {
    appointment: Appointment;
  }) {
    return (
      <div className="card row-xs">
        <ul className="list-group list-group-flush">
          <li className="list-group-item">Customer: <h5 className="card-title">{appointment.customer.first_name} {appointment.customer.last_name}</h5></li>
          {appointment.interpreter && <li className="list-group-item">Interpreter: <h5>{appointment.interpreter.first_name} {appointment.interpreter.last_name}</h5></li>}
          <li className="list-group-item">Language: {appointment.language.language_name}</li>
          <li className="list-group-item">When: {appointment.planned_start_time}</li>
          <li className="list-group-item">Duration: {appointment.planned_duration}</li>
          <li className="list-group-item">Where: {appointment.location}</li>
          <li className="list-group-item">Company: {appointment.company}</li>
          <li className="list-group-item">Gender Preference: {appointment.gender_preference}</li>
        </ul>
        {appointment.interpreter && appointment.invoice_generated && <div className="card-footer"><p className="text-success">Invoice Generated</p></div>}
      </div>
    );    
}

export function TranslationComponent({
    translation,
  }: {
    translation: Translation;
  }) {
    return (
      <div className="card row-xs">
        <ul className="list-group list-group-flush">
          <li className="list-group-item">Customer: <h5 className="card-title">{translation.customer.first_name} {translation.customer.last_name}</h5></li>
          {translation.interpreter && <li className="list-group-item">Interpreter: <h5>{translation.interpreter.first_name} {translation.interpreter.last_name}</h5></li>}
          <li className="list-group-item">Language: {translation.language.language_name}</li>
          <li className="list-group-item">Company: {translation.company}</li>
          <li className="list-group-item">Word count: {translation.word_count}</li>
          {translation.interpreter && translation.invoice_generated && <div className="card-footer"><p className="text-success">Invoice Generated</p></div>}
        </ul>
      </div>
    );    
}

export function TranslationInterpreterComponent({
  selectedTranslation,
  interpreter,
}: {
  selectedTranslation: Translation;
  interpreter: Interpreter;
}) {
  return (
      <div className="card row-xs">
        <ul className="list-group list-group-flush">
          <li className="list-group-item"><h5 className="card-title">{interpreter.first_name} {interpreter.last_name}</h5></li>
          <li className="list-group-item">Email: {interpreter.email}</li>
          <li className="list-group-item">Phone Number: {interpreter.phone_number ? interpreter.phone_number : "None on File"}</li>
          <li className="list-group-item">Gender: {interpreter.gender}</li>
        </ul>
        {interpreter.offered_translations.includes(selectedTranslation.id) && (<div className="card-footer"><p className="text-success">Translation Offered</p></div>)}
      </div>
  );    
}

export function AppointmentInterpreterComponent({
  selectedAppointment,
  interpreter,
}: {
  selectedAppointment: Appointment;
  interpreter: Interpreter;
}) {
  return (
      <div className="card row-xs">
        <ul className="list-group list-group-flush">
          <li className="list-group-item"><h5 className="card-title">{interpreter.first_name} {interpreter.last_name}</h5></li>
          <li className="list-group-item">Email: {interpreter.email}</li>
          <li className="list-group-item">Phone Number: {interpreter.phone_number ? interpreter.phone_number : "None on File"}</li>
          <li className="list-group-item">Gender: {interpreter.gender}</li>
        </ul>
        {interpreter.offered_appointments.includes(selectedAppointment.id) && (<div className="card-footer"><p className="text-success">Appointment Offered</p></div>)}
      </div>
  );    
}