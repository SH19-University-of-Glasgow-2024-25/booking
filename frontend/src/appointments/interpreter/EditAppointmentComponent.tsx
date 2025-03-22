import { useState } from "react";
import apiClient from "../../utilities/apiClient";
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
  actual_start_time?: string;
  actual_duration?: string;
}

export default function EditAppointmentComponent({
    appointment,
    fetchAppointments
  }: {
    appointment: Appointment;
    fetchAppointments: () => void;
  }) {
    const [editMode, setEditMode] = useState<boolean>(false);
    const [appointmentEditValues, setAppointmentEditValues] = useState<Appointment>(appointment);
    const [errorElm, setErrorElm] = useState(<div></div>);

    const updateAppointment = () => {
      console.log("Updated Appointment: ", appointmentEditValues);
      const returnData = {
        appID : appointmentEditValues.id,
        appActualStartTime : appointmentEditValues.actual_start_time,
        appActualDuration : appointmentEditValues.actual_duration,
      }
      apiClient.post("/edit-appointments/", returnData)
        .then((res) => {
            console.log(res.data)
            if (res.data.status == "success") {
                console.log("Edit Successful:", res.data);
            } else if (res.data.status == "error") {
                setErrorElm(GenerateErrorDisplayElement(res.data.error));
            }
            fetchAppointments();
        })
        .catch((err) => {
            setErrorElm(GenerateErrorDisplayElement(err.response?.data.error));
        });
    }

    return (
            <div className="card row-xs">
              <ul className="list-group list-group-flush">
                <li className="list-group-item">
                  <div className="d-flex justify-content-between align-items-center">
                    <div>
                      {errorElm}
                      Customer: <h5 className="card-title">{appointment.customer.first_name} {appointment.customer.last_name}</h5>
                    </div>
                    {editMode ? 
                      <div>
                        <button onClick={() => {updateAppointment(); setEditMode(false);}} className="btn btn-lg p-0 btn-link link-success me-2">
                          <i className="bi bi-check-circle"></i>
                        </button>
                        <button onClick={() => {setEditMode(false);}} className="btn btn-lg p-0 btn-link link-danger">
                          <i className="bi bi-x-circle"></i>
                        </button>
                      </div>
                      :
                      <div>
                        <button
                        className="btn btn-primary"
                        onClick={() => setEditMode(true)}
                        >
                          <i className="bi bi-pencil-fill"></i> Edit
                        </button>
                      </div>
                    }
                  </div>
                </li>
                <li className="list-group-item">Language: {appointment.language.language_name}</li>
                <li className="list-group-item">When: {appointment.planned_start_time}</li>
                <li className="list-group-item">Duration: {appointment.planned_duration}</li>
                <li className="list-group-item">Where: {appointment.location}</li>
                <li className="list-group-item">Company: {appointment.company}</li>
                <li className="list-group-item">Gender Preference: {appointment.gender_preference}</li>
                <li className="list-group-item">
                  Actual Start:&nbsp;
                  {editMode ? 
                      <input
                        className="form-control"
                        type="time"
                        value={appointmentEditValues.actual_start_time}
                        onChange={(e) =>
                          setAppointmentEditValues({ ...appointmentEditValues, actual_start_time: e.target.value })
                        }
                      />
                      :
                      <>{appointment.actual_start_time ? appointment.actual_start_time : <>Unset</>}</>
                  }
                </li>
                <li className="list-group-item">
                  Actual Duration:&nbsp; 
                  {editMode ? 
                      <input
                        className="form-control"
                        type="time"
                        value={appointmentEditValues.actual_duration}
                        onChange={(e) =>
                          setAppointmentEditValues({ ...appointmentEditValues, actual_duration: e.target.value })
                        }
                      />
                      :
                      <>{appointment.actual_duration ? appointment.actual_duration : <>Unset</>}</>
                  }
                </li>
              </ul>
            </div>
    );    
}