import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Paper,
  TextField,
  Button,
  Grid,
  Alert,
  MenuItem,
} from '@mui/material';
import { useAuth } from '../../contexts/AuthContext';
import { proyectoService } from '../../services/proyectoService';
import { Proyecto } from '../../types';

const ProyectoForm: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState<Omit<Proyecto, 'id' | 'created_at' | 'updated_at'>>({
    titulo: '',
    descripcion: '',
    objetivo: '',
    metodologia: '',
    resultados_esperados: '',
    presupuesto: '',
    duracion: '',
    estado: 'borrador',
    tipo_proyecto: 'investigacion',
    area_conocimiento: '',
    palabras_clave: '',
    lider_id: user?.id || 0
  });

  useEffect(() => {
    if (id) {
      loadProyecto();
    }
  }, [id]);

  const loadProyecto = async () => {
    try {
      setLoading(true);
      const proyecto = await proyectoService.getProyecto(id!);
      setFormData({
        titulo: proyecto.titulo,
        descripcion: proyecto.descripcion,
        objetivo: proyecto.objetivo,
        metodologia: proyecto.metodologia,
        resultados_esperados: proyecto.resultados_esperados,
        presupuesto: proyecto.presupuesto,
        duracion: proyecto.duracion,
        estado: proyecto.estado,
        tipo_proyecto: proyecto.tipo_proyecto,
        area_conocimiento: proyecto.area_conocimiento,
        palabras_clave: proyecto.palabras_clave,
        lider_id: proyecto.lider_id
      });
    } catch (err) {
      setError('Error al cargar el proyecto');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setLoading(true);
      setError(null);
      
      if (id) {
        await proyectoService.updateProyecto(id, formData);
      } else {
        await proyectoService.createProyecto(formData);
      }
      
      navigate('/dashboard');
    } catch (err) {
      setError('Error al guardar el proyecto');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
        <Typography>Cargando...</Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        {id ? 'Editar Proyecto' : 'Nuevo Proyecto'}
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Paper sx={{ p: 3 }}>
        <form onSubmit={handleSubmit}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <TextField
                required
                fullWidth
                label="Título"
                name="titulo"
                value={formData.titulo}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                required
                fullWidth
                multiline
                rows={4}
                label="Descripción"
                name="descripcion"
                value={formData.descripcion}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                required
                fullWidth
                multiline
                rows={4}
                label="Objetivo"
                name="objetivo"
                value={formData.objetivo}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                required
                fullWidth
                multiline
                rows={4}
                label="Metodología"
                name="metodologia"
                value={formData.metodologia}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                required
                fullWidth
                multiline
                rows={4}
                label="Resultados Esperados"
                name="resultados_esperados"
                value={formData.resultados_esperados}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                required
                fullWidth
                label="Presupuesto"
                name="presupuesto"
                type="number"
                value={formData.presupuesto}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                required
                fullWidth
                label="Duración (meses)"
                name="duracion"
                type="number"
                value={formData.duracion}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                required
                fullWidth
                select
                label="Estado"
                name="estado"
                value={formData.estado}
                onChange={handleChange}
              >
                <MenuItem value="borrador">Borrador</MenuItem>
                <MenuItem value="en_revision">En Revisión</MenuItem>
                <MenuItem value="aprobado">Aprobado</MenuItem>
                <MenuItem value="rechazado">Rechazado</MenuItem>
                <MenuItem value="en_progreso">En Progreso</MenuItem>
                <MenuItem value="completado">Completado</MenuItem>
              </TextField>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                required
                fullWidth
                select
                label="Tipo de Proyecto"
                name="tipo_proyecto"
                value={formData.tipo_proyecto}
                onChange={handleChange}
              >
                <MenuItem value="investigacion">Investigación</MenuItem>
                <MenuItem value="desarrollo">Desarrollo</MenuItem>
                <MenuItem value="innovacion">Innovación</MenuItem>
              </TextField>
            </Grid>
            <Grid item xs={12}>
              <TextField
                required
                fullWidth
                label="Área de Conocimiento"
                name="area_conocimiento"
                value={formData.area_conocimiento}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                required
                fullWidth
                label="Palabras Clave"
                name="palabras_clave"
                value={formData.palabras_clave}
                onChange={handleChange}
                helperText="Separe las palabras clave con comas"
              />
            </Grid>
            <Grid item xs={12}>
              <Box sx={{ display: 'flex', gap: 2 }}>
                <Button
                  type="submit"
                  variant="contained"
                  color="primary"
                  disabled={loading}
                >
                  {id ? 'Actualizar' : 'Crear'} Proyecto
                </Button>
                <Button
                  variant="outlined"
                  onClick={() => navigate('/dashboard')}
                >
                  Cancelar
                </Button>
              </Box>
            </Grid>
          </Grid>
        </form>
      </Paper>
    </Container>
  );
};

export default ProyectoForm; 