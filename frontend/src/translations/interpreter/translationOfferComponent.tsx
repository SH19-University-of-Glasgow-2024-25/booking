import fetchProtectedFile from "../../utilities/fetchProtectedFile";
interface Translation {
    id: number;
    customer: {id:number, first_name:string, last_name:string};
    language: {id:number, language_name:string};
    word_count: number;
    company: string;
    document: string;
}

export function TranslationOfferComponent({
    translation,
    updateTranslation,
    setShowToast
  }: {
    translation: Translation;
    updateTranslation: (appointmentID: number, accept: boolean) => void;
    setShowToast: (value: boolean) => void;
  }) {
    let filename: string = translation?.document.replace("/media/translation_documents/", "");

    return (
      <>
      <div className="card row-xs">
        <ul className="list-group list-group-flush">
          <li className="list-group-item">Customer: <h5 className="card-title">{translation.customer.first_name} {translation.customer.last_name}</h5></li>
          <li className="list-group-item">Language: {translation.language.language_name}</li>
          <li className="list-group-item">Word count: {translation.word_count}</li>
          <li className="list-group-item">Company: {translation.company}</li>
          <li className="list-group-item"><strong>Document:</strong> <button className="btn btn-link p-0" onClick={() => fetchProtectedFile(filename)}><i className="bi bi-download me-2"></i>{filename}</button></li>
        </ul>

        <div className="card-footer">
          <button
              className="btn btn-outline-success me-2"
              data-testid="customer-request-accept-button"
              onClick={() => {updateTranslation(translation.id, true); setShowToast(true)}}
          >
              Accept
          </button>
          <button
              className="btn btn-outline-danger"
              data-testid="customer-request-decline-button"
              onClick={() => updateTranslation(translation.id, false)}
          >
              Decline
          </button>
        </div>
      </div>
    </>
        
    );    
}