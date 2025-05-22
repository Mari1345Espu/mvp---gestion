import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  Button,
  Box,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  Snackbar,
  Alert,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
} from '@mui/icons-material';
import { userService } from '../../services/userService';
import { User, UserCreate, UserUpdate } from '../../types';
import { SelectChangeEvent } from '@mui/material/Select';

const Users: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [dialogOpen, setDialogOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [formData, setFormData] = useState<UserCreate | UserUpdate>({
    nombre: '',
    email: '',
    telefono: '',
    password: '',
    rol_id: 1,
  });
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success' as 'success' | 'error',
  });

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    setLoading(true);
    try {
      const response = await userService.getUsers();
      setUsers(response.content);
    } catch (err) {
      setError('Error al cargar los usuarios');
    } finally {
      setLoading(false);
    }
  };

  const handleOpenDialog = (user?: User) => {
    if (user) {
      setSelectedUser(user);
      setFormData({
        nombre: user.nombre,
        email: user.email,
        telefono: user.telefono,
        rol_id: user.rol_id,
      });
    } else {
      setSelectedUser(null);
      setFormData({
        nombre: '',
        email: '',
        telefono: '',
        password: '',
        rol_id: 1,
      });
    }
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setSelectedUser(null);
    setFormData({
      nombre: '',
      email: '',
      telefono: '',
      password: '',
      rol_id: 1,
    });
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | { name?: string; value: unknown }> | SelectChangeEvent<number>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name as string]: name === 'rol_id' ? Number(value) : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (selectedUser) {
        await userService.updateUser(selectedUser.id, formData as UserUpdate);
        showSnackbar('Usuario actualizado exitosamente', 'success');
      } else {
        await userService.createUser(formData as UserCreate);
        showSnackbar('Usuario creado exitosamente', 'success');
      }
      handleCloseDialog();
      loadUsers();
    } catch (err) {
      showSnackbar('Error al guardar el usuario', 'error');
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('¿Está seguro de eliminar este usuario?')) {
      try {
        await userService.deleteUser(id);
        showSnackbar('Usuario eliminado exitosamente', 'success');
        loadUsers();
      } catch (err) {
        showSnackbar('Error al eliminar el usuario', 'error');
      }
    }
  };

  const handleToggleStatus = async (id: number, currentStatus: number) => {
    try {
      const newStatus = currentStatus === 1 ? 2 : 1;
      await userService.updateUserStatus(id, newStatus);
      showSnackbar('Estado actualizado exitosamente', 'success');
      loadUsers();
    } catch (err) {
      showSnackbar('Error al actualizar el estado', 'error');
    }
  };

  const showSnackbar = (message: string, severity: 'success' | 'error') => {
    setSnackbar({
      open: true,
      message,
      severity,
    });
  };

  const handleCloseSnackbar = () => {
    setSnackbar((prev) => ({ ...prev, open: false }));
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
          <Typography variant="h5" component="h1">
            Gestión de Usuarios
          </Typography>
          <Button
            variant="contained"
            color="primary"
            startIcon={<AddIcon />}
            onClick={() => handleOpenDialog()}
          >
            Nuevo Usuario
          </Button>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Nombre</TableCell>
                <TableCell>Email</TableCell>
                <TableCell>Teléfono</TableCell>
                <TableCell>Rol</TableCell>
                <TableCell>Estado</TableCell>
                <TableCell>Acciones</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {users.map((user) => (
                <TableRow key={user.id}>
                  <TableCell>{user.nombre}</TableCell>
                  <TableCell>{user.email}</TableCell>
                  <TableCell>{user.telefono}</TableCell>
                  <TableCell>
                    {user.rol_id === 1 ? 'Administrador' : 'Usuario'}
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={user.estado_id === 1 ? 'Activo' : 'Inactivo'}
                      color={user.estado_id === 1 ? 'success' : 'error'}
                      onClick={() => handleToggleStatus(user.id, user.estado_id)}
                    />
                  </TableCell>
                  <TableCell>
                    <IconButton
                      color="primary"
                      onClick={() => handleOpenDialog(user)}
                    >
                      <EditIcon />
                    </IconButton>
                    <IconButton
                      color="error"
                      onClick={() => handleDelete(user.id)}
                    >
                      <DeleteIcon />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>

        <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
          <DialogTitle>
            {selectedUser ? 'Editar Usuario' : 'Nuevo Usuario'}
          </DialogTitle>
          <form onSubmit={handleSubmit}>
            <DialogContent>
              <TextField
                fullWidth
                margin="normal"
                label="Nombre"
                name="nombre"
                value={formData.nombre}
                onChange={handleChange}
                required
              />
              <TextField
                fullWidth
                margin="normal"
                label="Email"
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
              />
              <TextField
                fullWidth
                margin="normal"
                label="Teléfono"
                name="telefono"
                value={formData.telefono}
                onChange={handleChange}
                required
              />
              {!selectedUser && (
                <TextField
                  fullWidth
                  margin="normal"
                  label="Contraseña"
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  required
                />
              )}
              <FormControl fullWidth margin="normal">
                <InputLabel>Rol</InputLabel>
                <Select
                  name="rol_id"
                  value={formData.rol_id}
                  onChange={handleChange}
                  required
                >
                  <MenuItem value={1}>Administrador</MenuItem>
                  <MenuItem value={2}>Usuario</MenuItem>
                </Select>
              </FormControl>
            </DialogContent>
            <DialogActions>
              <Button onClick={handleCloseDialog}>Cancelar</Button>
              <Button type="submit" variant="contained" color="primary">
                {selectedUser ? 'Actualizar' : 'Crear'}
              </Button>
            </DialogActions>
          </form>
        </Dialog>

        <Snackbar
          open={snackbar.open}
          autoHideDuration={6000}
          onClose={handleCloseSnackbar}
        >
          <Alert
            onClose={handleCloseSnackbar}
            severity={snackbar.severity}
            sx={{ width: '100%' }}
          >
            {snackbar.message}
          </Alert>
        </Snackbar>
      </Box>
    </Container>
  );
};

export default Users; 