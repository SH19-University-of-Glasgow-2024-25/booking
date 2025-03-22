export interface Customer {
    first_name: string;
    last_name: string;
    organisation: string;
    phone_number: string;
    email: string;
    address: string;
    postcode: string;
}

export function CustomerRequest({
    customer,
    actionRequest,
  }: {
    customer: Customer;
    actionRequest: (email: string, accepted: boolean) => void;
  }) {
    return (
        <div className="card row-xs">
            <div className="card-body">
                <h4 className="card-title">{customer.first_name} {customer.last_name}</h4>
                <h5>{customer.organisation}</h5>
            </div>
            
            <ul className="list-group list-group-flush">
                <li className="list-group-item">Email: {customer.email}</li>
                <li className="list-group-item">Phone Number: {customer.phone_number}</li>
                <li className="list-group-item">Address: {customer.address}</li>
                <li className="list-group-item">Postcode: {customer.postcode}</li>
            </ul>

            <div className="card-footer">
                <button
                    className="btn btn-outline-success me-2"
                    data-testid="customer-request-accept-button"
                    onClick={() => actionRequest(customer.email, true)}
                >
                    Accept
                </button>
                <button
                    className="btn btn-outline-danger"
                    data-testid="customer-request-decline-button"
                    onClick={() => actionRequest(customer.email, false)}
                >
                    Decline
                </button>
            </div>
            
        </div>
    );    
}