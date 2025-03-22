import { useState, useEffect } from "react";
import {Customer, CustomerRequest} from './CustomerRequest'
import apiClient from '../../utilities/apiClient';
import {GenerateErrorDisplayElement} from "../../utilities/Error";

function RequestAccept() {

    const [customers, setCustomers] = useState<Customer[] | null>(null);
    const [errorElm, setErrorElm] = useState(<div></div>);

    const fetchData = () => {
        apiClient.get("/needs-approval/")
            .then((res) => {
                if (res.data.status == "success") {
                    console.log("Request Retrieval Successful:", res.data);
                    setCustomers(res.data.result.customers);
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
        const refreshRequests = setInterval(fetchData, 15000);
        return () => clearInterval(refreshRequests);
    }, []);

    const actionRequest = (email: string, accepted: boolean) => {
        const returnData = {
            email: email,
            accepted: accepted,
        }
        apiClient.post("/approve/", returnData)
            .then((res) => {
                if (res.data.status == "success") {
                    console.log("Request Response Actioned:", res.data);
                    fetchData();
                } else if (res.data.status == "error") {
                    setErrorElm(GenerateErrorDisplayElement(res.data.error));
                }
            })
            .catch((err) => {
                setErrorElm(GenerateErrorDisplayElement(err.response?.data.error));
            });
    }
    
    return (
            <div className="main-content container d-md-flex justify-content-center pt-3">
                <div className="col">
                    {errorElm}
                    <h3>Customer Requests</h3>
                    <div className="d-flex flex-wrap">
                        {customers && customers.length !== 0 ? (customers.map((customer, index) => {
                            return (
                                <div key={"div"+index} className="m-2">
                                    <CustomerRequest key={"request"+index} customer={customer} actionRequest={actionRequest}/>
                                </div>
                            );
                        })) : customers ? <p>No customers requests!</p> : <p>Customer requests loading...</p>
                        }
                    </div>
                </div>
                <div className="col-md-3">
                    <div className="px-3 pt-2 ms-4 border-start border-danger bg-body-tertiary mt-3 pb-2">
                        Once a customer request is declined, it will disappear and cannot be accepted again, unless 
                        the user makes another request.
                    </div>
                    <div className="px-3 pt-2 ms-4 border-start bg-body-tertiary mt-3 pb-2">
                        <h5>Or you can...</h5>

                        { /* TODO: Alter routing so that these can be made into working links. Currently redirect to home due to 404. */ }
                        
                        <a href="/admin/create-account" className="link-secondary d-block mb-2">Admin: Create Accounts</a>
                        
                        <a href="/admin/profile" className="link-secondary d-block mb-2">Admin: Edit User Profiles</a>
                    </div>
                </div>
            </div>
    );    
}

export default RequestAccept;