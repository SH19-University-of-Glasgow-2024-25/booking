import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Header from './Header';
import Landing from './Landing';
import AccountLanding from './AccountLanding';
import ProtectedRoute from '../utilities/ProtectedRoute';
import AccountContext from '../utilities/authenticationContext';
import AdminPage from '../admin/Admin';
import Verification from '../verification/Verification';
import ResendVerification from '../verification/ResendVerification';
import Footer from './Footer';
import AppointmentsPage from '../appointments/Appointments';
import TranslationsPage from '../translations/Translations';
import AppointmentManagementPage from '../appointments/interpreter/appointmentsManagement';
import SendPasswordReset from '../utilities/sendPasswordReset';
import NewPassword from '../utilities/NewPassword'; // Correct import
import { EditProfileSelf } from '../profile/EditProfileSelf';
import InterpreterAcceptedTranslations from '../translations/interpreter/translationManagement'
import AppointmentTranslationContext from '../appointments/appointmentTranslationContext';


const App: React.FC = () => {
    // global account type context, allowing restriction of context without constant API calls
    const [accountType, setAccountType] = useState<string | null>(null);

    const [appointmentOrTranslation, setAppointmentOrTranslation] = useState<"Appointments" | "Translations">("Appointments");

    return (
        <AccountContext.Provider value={{ accountType, setAccountType }}>
        <AppointmentTranslationContext.Provider value={{ appointmentOrTranslation, setAppointmentOrTranslation }}>
        <Router>
            <Header />
            <div className="app-container">
                <Routes>
                    {/* Public */}
                    <Route path="/authentication/login" element={<AccountLanding registerType='L'/>} />
                    <Route path="/authentication/request-customer" element={<AccountLanding registerType='C'/>} />
                    <Route path="/authentication/forgot-password" element={<AccountLanding registerType='F'/>} />
                    <Route path="/verification-email" element={<Verification/>}/>
                    <Route path="/authentication/resend-email-verification" element={<ResendVerification />}/>
                    <Route path="/send-password-reset" element={<SendPasswordReset />} /> 
                    <Route path="/update-password/:uidb64/:token" element={<NewPassword />} />
                    
                    {/* Protected */}
                    <Route 
                        path="/home" 
                        element={
                            <ProtectedRoute admin_access customer_access interpreter_access>
                                <Landing />
                            </ProtectedRoute>
                        } 
                    />
                    <Route 
                        path="/admin" 
                        element={
                            <ProtectedRoute admin_access>
                                <AdminPage/>
                            </ProtectedRoute>
                            } 
                    />
                    <Route 
                        path="/appointments" 
                        element={
                            <ProtectedRoute admin_access customer_access interpreter_access>
                                <AppointmentsPage/>
                            </ProtectedRoute>
                            } 
                    />
                    <Route
                        path="/profile"
                        element = {
                            <ProtectedRoute admin_access customer_access interpreter_access>
                                <EditProfileSelf/>
                            </ProtectedRoute>
                        }
                    />
                    <Route 
                        path="/translations" 
                        element={
                            <ProtectedRoute admin_access customer_access interpreter_access>
                                <TranslationsPage />
                            </ProtectedRoute>
                        } 
                    />
                    <Route
                        path="/appointments/accepted"
                        element={
                            <ProtectedRoute interpreter_access>
                                <AppointmentManagementPage/>
                            </ProtectedRoute>
                        }
                    />
                    <Route
                        path="/translations/accepted"
                        element={
                            <ProtectedRoute interpreter_access>
                                <InterpreterAcceptedTranslations/>
                            </ProtectedRoute>
                        }
                    />
                    <Route 
                        path="/home" 
                        element={
                            <ProtectedRoute admin_access customer_access interpreter_access>
                                <Landing />
                            </ProtectedRoute>
                        } 
                    />
                    {/* Fallback */}
                    <Route path="*" element={<Navigate to="/authentication/login" />} />
                </Routes>
            </div>
            <Footer/>
        </Router>
        </AppointmentTranslationContext.Provider>
        </AccountContext.Provider>
    );
};

export default App;
