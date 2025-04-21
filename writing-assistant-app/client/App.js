import React from 'react';
import { Provider } from 'react-redux';
import { PersistGate } from 'redux-persist/integration/react';
import { store, persistor } from './store/store';
import AppNavigator from './navigation/AppNavigator';
import { AuthProvider } from './contexts/AuthContext';
import { AIProvider } from './contexts/AIStateContext';

export default function App() {
  return (
    <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        <AuthProvider>
          <AIProvider>
            <AppNavigator />
          </AIProvider>
        </AuthProvider>
      </PersistGate>
    </Provider>
  );
}
