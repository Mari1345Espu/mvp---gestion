import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
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
  Box,
  Chip,
  Snackbar,
  Alert,
  Grid,
} from '@mui/material';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  Add as AddIcon,
  Visibility as ViewIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import projectService, { Project, ProjectCreate, ProjectUpdate } from '../../services/projectService';

const Projects = () => {
  const navigate = useNavigate();
  const [projects, setProjects] = useState<Project[]>([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);
  const [formData, setFormData] = useState<ProjectCreate>({
    titulo: '',
    objetivos: '',
    convocatoria_id: 0,
    grupo_investigacion_id: 0,
    linea_investigacion_id: 0,
    extension_id: 0,
    estado_id: 0,
    fecha_inicio: '',
  });
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success' as 'success' | 'error',
  });

  // Estados para los datos de los selectores
  const [convocatorias, setConvocatorias] = useState<any[]>([]);
  const [gruposInvestigacion, setGruposInvestigacion] = useState<any[]>([]);
  const [lineasInvestigacion, setLineasInvestigacion] = useState<any[]>([]);
  const [extensiones, setExtensiones] = useState<any[]>([]);
  const [estados, setEstados] = useState<any[]>([]);
  const [evaluadoresExternos, setEvaluadoresExternos] = useState<any[]>([]);

  useEffect(() => {
    loadProjects();
    loadSelectData();
  }, []);

  const loadSelectData = async () => {
    try {
      const [
        convocatoriasData,
        gruposData,
        lineasData,
        extensionesData,
        estadosData,
        evaluadoresData,
      ] = await Promise.all([
        projectService.getConvocatorias(),
        projectService.getGruposInvestigacion(),
        projectService.getLineasInvestigacion(),
        projectService.getExtensiones(),
        projectService.getEstados(),
        projectService.getEvaluadoresExternos(),
      ]);

      setConvocatorias(convocatoriasData);
      setGruposInvestigacion(gruposData);
      setLineasInvestigacion(lineasData);
      setExtensiones(extensionesData);
      setEstados(estadosData);
      setEvaluadoresExternos(evaluadoresData);
    } catch (error) {
      console.error('Error al cargar datos de selección:', error);
      showSnackbar('Error al cargar datos de selección', 'error');
    }
  };

  const loadProjects = async () => {
    try {
      const data = await projectService.getProjects();
      setProjects(data);
    } catch (error) {
      console.error('Error al cargar proyectos:', error);
      showSnackbar('Error al cargar proyectos', 'error');
    }
  };

  const handleOpenDialog = (project?: Project) => {
    if (project) {
      setSelectedProject(project);
      setFormData({
        titulo: project.titulo,
        objetivos: project.objetivos,
        convocatoria_id: project.convocatoria_id,
        grupo_investigacion_id: project.grupo_investigacion_id,
        linea_investigacion_id: project.linea_investigacion_id,
        extension_id: project.extension_id,
        estado_id: project.estado_id,
        fecha_inicio: project.fecha_inicio,
        evaluador_externo_id: project.evaluador_externo_id || undefined,
      });
    } else {
      setSelectedProject(null);
      setFormData({
        titulo: '',
        objetivos: '',
        convocatoria_id: 0,
        grupo_investigacion_id: 0,
        linea_investigacion_id: 0,
        extension_id: 0,
        estado_id: 0,
        fecha_inicio: '',
      });
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setSelectedProject(null);
  };

  const handleSubmit = async () => {
    try {
      if (selectedProject) {
        const updateData: ProjectUpdate = {
          ...formData,
        };
        await projectService.updateProject(selectedProject.id, updateData);
        showSnackbar('Proyecto actualizado exitosamente');
      } else {
        await projectService.createProject(formData);
        showSnackbar('Proyecto creado exitosamente');
      }
      handleCloseDialog();
      loadProjects();
    } catch (error) {
      console.error('Error al guardar proyecto:', error);
      showSnackbar('Error al guardar proyecto', 'error');
    }
  };

  const handleDelete = async (projectId: number) => {
    if (window.confirm('¿Está seguro de eliminar este proyecto?')) {
      try {
        await projectService.deleteProject(projectId);
        showSnackbar('Proyecto eliminado exitosamente');
        loadProjects();
      } catch (error) {
        console.error('Error al eliminar proyecto:', error);
        showSnackbar('Error al eliminar proyecto', 'error');
      }
    }
  };

  const handleViewDetails = (projectId: number) => {
    navigate(`/admin/projects/${projectId}`);
  };

  const showSnackbar = (message: string, severity: 'success' | 'error' = 'success') => {
    setSnackbar({
      open: true,
      message,
      severity,
    });
  };

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Gestión de Proyectos
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
        >
          Nuevo Proyecto
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Título</TableCell>
              <TableCell>Convocatoria</TableCell>
              <TableCell>Grupo de Investigación</TableCell>
              <TableCell>Estado</TableCell>
              <TableCell>Fecha Inicio</TableCell>
              <TableCell>Evaluador</TableCell>
              <TableCell>Acciones</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {projects.map((project) => (
              <TableRow key={project.id}>
                <TableCell>{project.titulo}</TableCell>
                <TableCell>{project.convocatoria}</TableCell>
                <TableCell>{project.grupo_investigacion}</TableCell>
                <TableCell>
                  <Chip
                    label={project.estado}
                    color={project.estado === 'Activo' ? 'success' : 'error'}
                    size="small"
                  />
                </TableCell>
                <TableCell>{project.fecha_inicio}</TableCell>
                <TableCell>{project.evaluador_externo}</TableCell>
                <TableCell>
                  <IconButton
                    color="primary"
                    onClick={() => handleViewDetails(project.id)}
                  >
                    <ViewIcon />
                  </IconButton>
                  <IconButton
                    color="primary"
                    onClick={() => handleOpenDialog(project)}
                  >
                    <EditIcon />
                  </IconButton>
                  <IconButton
                    color="error"
                    onClick={() => handleDelete(project.id)}
                  >
                    <DeleteIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        <DialogTitle>
          {selectedProject ? 'Editar Proyecto' : 'Nuevo Proyecto'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <TextField
                  label="Título"
                  value={formData.titulo}
                  onChange={(e) =>
                    setFormData({ ...formData, titulo: e.target.value })
                  }
                  fullWidth
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  label="Objetivos"
                  value={formData.objetivos}
                  onChange={(e) =>
                    setFormData({ ...formData, objetivos: e.target.value })
                  }
                  multiline
                  rows={4}
                  fullWidth
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel>Convocatoria</InputLabel>
                  <Select
                    value={formData.convocatoria_id}
                    label="Convocatoria"
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        convocatoria_id: Number(e.target.value),
                      })
                    }
                  >
                    {convocatorias.map((convocatoria) => (
                      <MenuItem key={convocatoria.id} value={convocatoria.id}>
                        {convocatoria.nombre}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel>Grupo de Investigación</InputLabel>
                  <Select
                    value={formData.grupo_investigacion_id}
                    label="Grupo de Investigación"
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        grupo_investigacion_id: Number(e.target.value),
                      })
                    }
                  >
                    {gruposInvestigacion.map((grupo) => (
                      <MenuItem key={grupo.id} value={grupo.id}>
                        {grupo.nombre}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel>Línea de Investigación</InputLabel>
                  <Select
                    value={formData.linea_investigacion_id}
                    label="Línea de Investigación"
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        linea_investigacion_id: Number(e.target.value),
                      })
                    }
                  >
                    {lineasInvestigacion.map((linea) => (
                      <MenuItem key={linea.id} value={linea.id}>
                        {linea.nombre}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel>Extensión</InputLabel>
                  <Select
                    value={formData.extension_id}
                    label="Extensión"
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        extension_id: Number(e.target.value),
                      })
                    }
                  >
                    {extensiones.map((extension) => (
                      <MenuItem key={extension.id} value={extension.id}>
                        {extension.nombre}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel>Estado</InputLabel>
                  <Select
                    value={formData.estado_id}
                    label="Estado"
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        estado_id: Number(e.target.value),
                      })
                    }
                  >
                    {estados.map((estado) => (
                      <MenuItem key={estado.id} value={estado.id}>
                        {estado.nombre}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  label="Fecha de Inicio"
                  type="date"
                  value={formData.fecha_inicio}
                  onChange={(e) =>
                    setFormData({ ...formData, fecha_inicio: e.target.value })
                  }
                  fullWidth
                  InputLabelProps={{
                    shrink: true,
                  }}
                />
              </Grid>
              <Grid item xs={12}>
                <FormControl fullWidth>
                  <InputLabel>Evaluador Externo</InputLabel>
                  <Select
                    value={formData.evaluador_externo_id || ''}
                    label="Evaluador Externo"
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        evaluador_externo_id: Number(e.target.value),
                      })
                    }
                  >
                    {evaluadoresExternos.map((evaluador) => (
                      <MenuItem key={evaluador.id} value={evaluador.id}>
                        {evaluador.nombre}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancelar</Button>
          <Button onClick={handleSubmit} variant="contained">
            {selectedProject ? 'Actualizar' : 'Crear'}
          </Button>
        </DialogActions>
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
    </Container>
  );
};

export default Projects; 