import ProtectedContent from '../utilities/ProtectedContent';
import TranslationsAcceptancePage from "./interpreter/translationAcceptance";
import TranslationsCreationPage from "./customer/translationCreation";

function TranslationsPage() {
    return (
        <>
        
            {/* <ProtectedContent admin_access>
                <TranslationsManagementPage/> 
            </ProtectedContent>  */}
            <ProtectedContent interpreter_access>
                <TranslationsAcceptancePage/>
            </ProtectedContent>
            <ProtectedContent customer_access>
                <div className="navbar green-texture" data-bs-theme="dark">
                    <div className="container">
                        <div className="navbar-inner">
                            <div className="navbar-brand">
                                Translations
                            </div>
                        </div>
                    </div>
                </div>
                <TranslationsCreationPage/>
            </ProtectedContent>
        
        </>
    );    
}

export default TranslationsPage;