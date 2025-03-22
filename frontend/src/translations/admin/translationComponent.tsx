import fetchProtectedFile from "../../utilities/fetchProtectedFile";
interface Translation {
    pk: number;
    document: string;
    customer: string;
    word_count: number;
    language: string;
    company: string;
}

function TranslationComponent({
    translation,
}: {
    translation: Translation;
}) {
    return (
        <div className="translation-selection">
            <h3>{translation.customer}</h3>
            <p>Language: {translation.language}</p>
            <p>Document: {translation.document.replace("/media/translation_documents/", "")}</p>
            <p>Word Count: {translation.word_count}</p>
            <p>Company: {translation.company}</p>
            <p><button onClick={() => fetchProtectedFile(translation.document.replace("/media/translation_documents/", ""))}>Download</button></p>
        </div>
    );
}

export default TranslationComponent