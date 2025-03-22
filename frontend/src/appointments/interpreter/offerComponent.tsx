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

export function OfferComponent({
    appointment,
    updateAppointment,
    setShowToast
  }: {
    appointment: Appointment;
    updateAppointment: (appointmentID: number, accept: boolean) => void;
    setShowToast: (value: boolean) => void;
  }) {

    return (
      <>
        <div className="card row-xs">
          <ul className="list-group list-group-flush">
            <li className="list-group-item">Customer: <h5 className="card-title">{appointment.customer.first_name} {appointment.customer.last_name}</h5></li>
            <li className="list-group-item">Language: {appointment.language.language_name}</li>
            <li className="list-group-item">When: {appointment.planned_start_time}</li>
            <li className="list-group-item">Duration: {appointment.planned_duration}</li>
            <li className="list-group-item">Where: {appointment.location}</li>
            <li className="list-group-item">Company: {appointment.company}</li>
            <li className="list-group-item">Gender Preference: {appointment.gender_preference}</li>
          </ul>

          <div className="card-footer">
            <button
                className="btn btn-outline-success me-2"
                data-testid="customer-request-accept-button"
                onClick={() => {updateAppointment(appointment.id, true); setShowToast(true)}}
            >
                Accept
            </button>
            <button
                className="btn btn-outline-danger"
                data-testid="customer-request-decline-button"
                onClick={() => {updateAppointment(appointment.id, false);}}
            >
                Decline
            </button>
          </div>
        </div>
      </>
    );    
}

