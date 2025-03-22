import { useEffect, useState } from "react";
import apiClient from "../../utilities/apiClient";
import {GenerateErrorDisplayElement} from "../../utilities/Error";
import TranslationComponent from "./translationComponent";

interface Translation {
    pk: number;
    document: string;
    customer: string;
    word_count: number;
    language: string;
    company: string;
}

function TranslationsManagementPage() {
    const [translations, setTransaltions] = useState<Translation[] | null>(null);
    const [errorElm, setErrorElm] = useState(<div></div>);

    const fetchData = () => {
        apiClient.get("/all-translations/")
            .then((res) => {
                if (res.data.status == "success") {
                    console.log("Request Retrieval Successful:", res.data);
                    setTransaltions(res.data.result.appointments);
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

    return (
        <>
        <div className="main-container container">
            <main className="main-content">
                <header className="content-header">
                    <h1>Translation Management</h1>
                </header>

                {errorElm}

                <section className="content-section">
                    <h2>Select a translation:</h2>
                    {translations?.map((app) => (
                        <TranslationComponent translation={app} key={app.pk}/>
                    ))}
                </section>
            </main>
        </div>
        </>
    );   
}

export default TranslationsManagementPage;