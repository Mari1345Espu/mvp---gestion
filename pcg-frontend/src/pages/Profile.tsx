import React, { useState } from 'react';
import { userService } from '../services/userService';
import { User } from '../types';

interface ProfileFormData {
  nombre: string;
  email: string;
  telefono: string;
}

const Profile: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

  const handleUpdateProfile = async (formData: ProfileFormData) => {
    try {
      const response = await userService.updateUserProfile(formData);
      setUser(response);
      setSnackbar({ open: true, message: 'Perfil actualizado correctamente', severity: 'success' });
    } catch (err) {
      console.error('Error al actualizar el perfil:', err);
      setSnackbar({ open: true, message: 'Hubo un error al actualizar el perfil', severity: 'error' });
    }
  };

  return (
    <div>
      {/* Render your component content here */}
    </div>
  );
};

export default Profile; 