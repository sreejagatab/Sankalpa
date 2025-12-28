import React, { createContext, useContext, useState, ReactNode, useCallback } from 'react';

// Alert types
export type AlertType = 'success' | 'error' | 'warning' | 'info';

// Alert interface
export interface Alert {
  id: string;
  type: AlertType;
  message: string;
  title?: string;
  autoClose?: boolean;
  duration?: number;
}

// Alert context interface
interface AlertContextType {
  alerts: Alert[];
  addAlert: (alert: Omit<Alert, 'id'>) => string;
  removeAlert: (id: string) => void;
  clearAlerts: () => void;
}

// Create context
const AlertContext = createContext<AlertContextType | undefined>(undefined);

// Hook to use the alert context
export function useAlerts() {
  const context = useContext(AlertContext);
  if (context === undefined) {
    throw new Error('useAlerts must be used within an AlertProvider');
  }
  return context;
}

// Generate a unique ID for each alert
function generateId(): string {
  return Math.random().toString(36).substring(2, 11);
}

interface AlertProviderProps {
  children: ReactNode;
}

export function GlobalAlertProvider({ children }: AlertProviderProps) {
  const [alerts, setAlerts] = useState<Alert[]>([]);

  // Add a new alert
  const addAlert = useCallback((alert: Omit<Alert, 'id'>): string => {
    const id = generateId();
    const newAlert: Alert = {
      id,
      autoClose: true,
      duration: 5000,
      ...alert,
    };

    setAlerts((currentAlerts) => [...currentAlerts, newAlert]);

    // Auto-close the alert if specified
    if (newAlert.autoClose) {
      setTimeout(() => {
        removeAlert(id);
      }, newAlert.duration);
    }

    return id;
  }, []);

  // Remove an alert by ID
  const removeAlert = useCallback((id: string) => {
    setAlerts((currentAlerts) => currentAlerts.filter((alert) => alert.id !== id));
  }, []);

  // Clear all alerts
  const clearAlerts = useCallback(() => {
    setAlerts([]);
  }, []);

  // Context value
  const value = {
    alerts,
    addAlert,
    removeAlert,
    clearAlerts,
  };

  return <AlertContext.Provider value={value}>{children}</AlertContext.Provider>;
}

export default GlobalAlertProvider;