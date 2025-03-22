export interface ErrorResponseData {
    "error-message"?: string,
    "error-list"?: [string],
    "error-code"?: string,
    "error-data"?: object
}

export function GenerateErrorDisplayElement(response_data: ErrorResponseData): JSX.Element {
    let error_element: JSX.Element = <span></span>;
    if (response_data != undefined) {
        if (response_data["error-list"])
            error_element = <div>Errors:<ul>
                {Object.entries(response_data["error-list"]).map((field, key) => (
                <li key={key}>{field.toString().split(",")[0]}: {field.toString().split(",")[1]}</li>
                ))}
            </ul>
            </div>
        else if (response_data["error-message"])
            error_element = <div>
                <span className="error-detail">Error: {response_data["error-message"]}</span>
            </div>;
        else if (response_data["error-code"])
            error_element = <div>
                <span className="error-detail">An error has occurred. Error code: {response_data["error-code"]}</span>
            </div>;
        else
            error_element = <div>
                <span className="error-detail">An unknown error has occurred.</span>
            </div>;
        return <div className="alert alert-danger my-3" data-testid="error-message"> 
            {error_element}
        </div>
    } else {
        return <div className="alert alert-danger my-3" data-testid="error-message">
            <span className="error-detail">An unknown error has occurred.</span>
        </div>;
    }
}