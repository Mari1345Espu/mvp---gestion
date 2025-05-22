import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  CardMedia,
  TextField,
  MenuItem,
  Box,
  Chip,
  CircularProgress,
  Alert,
  Button,
  Select,
  SelectChangeEvent,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { proyectoService } from '../services/proyectoService';
import { programaService } from '../services/programaService';
import { Proyecto, Programa } from '../types';

const Home: React.FC = () => {
  const navigate = useNavigate();
  const [proyectos, setProyectos] = useState<Proyecto[]>([]);
  const [programas, setProgramas] = useState<Programa[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState({
    search: '',
    estado: '',
    programa: '',
  });

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        setError(null);
        const [projectsResponse, programsResponse] = await Promise.all([
          proyectoService.getProyectos(0, 10),
          programaService.getProgramas()
        ]);
        setProyectos(projectsResponse.content);
        setProgramas(programsResponse);
      } catch (err) {
        console.error('Error al cargar datos:', err);
        setError('No se pudieron cargar los datos. Por favor, intente nuevamente más tarde.');
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setFilters((prev) => ({
      ...prev,
      search: event.target.value,
    }));
  };

  const handleSelectChange = (event: SelectChangeEvent) => {
    const { name, value } = event.target;
    setFilters((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const filteredProjects = proyectos.filter(proyecto => {
    const matchesSearch = proyecto.nombre.toLowerCase().includes(filters.search.toLowerCase()) ||
                         proyecto.descripcion.toLowerCase().includes(filters.search.toLowerCase());
    const matchesPrograma = !filters.programa || proyecto.programa.id.toString() === filters.programa;
    const matchesEstado = !filters.estado || proyecto.estado === filters.estado;
    return matchesSearch && matchesPrograma && matchesEstado;
  });

  const estados = ['Activo', 'En Progreso', 'Completado', 'Cancelado'];

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
        <Button
          variant="contained"
          color="primary"
          onClick={() => window.location.reload()}
          sx={{ mt: 2 }}
        >
          Reintentar
        </Button>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Biblioteca de Proyectos
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" paragraph>
        Explora nuestra colección de proyectos y encuentra el que mejor se adapte a tus necesidades
      </Typography>

      {/* Filtros */}
      <Grid container spacing={2} sx={{ mb: 4 }}>
        <Grid item xs={12} md={4}>
          <TextField
            fullWidth
            label="Buscar proyectos"
            value={filters.search}
            onChange={handleSearchChange}
            placeholder="Buscar por nombre o descripción..."
          />
        </Grid>
        <Grid item xs={12} md={4}>
          <Select
            fullWidth
            label="Estado"
            name="estado"
            value={filters.estado}
            onChange={handleSelectChange}
          >
            <MenuItem value="">Todos</MenuItem>
            {estados.map((estado) => (
              <MenuItem key={estado} value={estado}>
                {estado}
              </MenuItem>
            ))}
          </Select>
        </Grid>
        <Grid item xs={12} md={4}>
          <Select
            fullWidth
            label="Programa"
            name="programa"
            value={filters.programa}
            onChange={handleSelectChange}
          >
            <MenuItem value="">Todos</MenuItem>
            {programas.map((programa) => (
              <MenuItem key={programa.id} value={programa.id.toString()}>
                {programa.nombre}
              </MenuItem>
            ))}
          </Select>
        </Grid>
      </Grid>

      {/* Lista de proyectos */}
      <Grid container spacing={3}>
        {filteredProjects.length === 0 ? (
          <Grid item xs={12}>
            <Alert severity="info">
              No se encontraron proyectos que coincidan con los criterios de búsqueda.
            </Alert>
          </Grid>
        ) : (
          filteredProjects.map((proyecto) => (
            <Grid item key={proyecto.id} xs={12} sm={6} md={4}>
              <Card
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  cursor: 'pointer',
                  '&:hover': {
                    boxShadow: 6,
                  },
                }}
                onClick={() => navigate(`/dashboard/proyectos/${proyecto.id}`)}
              >
                <CardMedia
                  component="img"
                  height="140"
                  image={proyecto.imagen || '/placeholder.jpg'}
                  alt={proyecto.nombre}
                />
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography gutterBottom variant="h6" component="h2">
                    {proyecto.nombre}
                  </Typography>
                  <Typography
                    variant="body2"
                    color="text.secondary"
                    sx={{
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      display: '-webkit-box',
                      WebkitLineClamp: 3,
                      WebkitBoxOrient: 'vertical',
                    }}
                  >
                    {proyecto.descripcion}
                  </Typography>
                  <Box sx={{ mt: 2 }}>
                    <Chip
                      label={proyecto.estado}
                      color={
                        proyecto.estado === 'Activo'
                          ? 'success'
                          : proyecto.estado === 'En Progreso'
                          ? 'primary'
                          : proyecto.estado === 'Completado'
                          ? 'info'
                          : 'error'
                      }
                      size="small"
                    />
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))
        )}
      </Grid>
    </Container>
  );
};

export default Home; 