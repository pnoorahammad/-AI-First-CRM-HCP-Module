import React, { useEffect } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { useDispatch, useSelector } from 'react-redux';
import {
  Box,
  TextField,
  Button,
  Grid,
  MenuItem,
  CircularProgress,
  Alert,
  } from '@mui/material';
import { createInteraction, clearInteractionError } from '../../store/slices/interactionSlice';
import { fetchHCPs } from '../../store/slices/hcpSlice';
import { AppDispatch, RootState } from '../../store/store';
import { InteractionCreate } from '../../types/interaction';

const visitTypes = ['In-person', 'Virtual', 'Phone'];

export const StructuredForm: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { hcps, isLoading: hcpsLoading } = useSelector((state: RootState) => state.hcp);
  const { isLoading, error } = useSelector((state: RootState) => state.interactions);

  const { control, handleSubmit, reset, formState: { errors } } = useForm<InteractionCreate>({
    defaultValues: {
      hcp_id: 0,
      date: new Date().toISOString().split('T')[0],
      time: new Date().toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' }),
      visit_type: 'In-person',
      products_discussed: [],
      samples_given: [],
      feedback: '',
      notes: '',
      follow_up_date: '',
      source: 'form'
    }
  });

  useEffect(() => {
    dispatch(fetchHCPs());
    return () => {
      dispatch(clearInteractionError());
    };
  }, [dispatch]);

  const onSubmit = async (data: InteractionCreate) => {
    // Process string arrays from comma-separated input
    const processedData = {
      ...data,
      products_discussed: typeof data.products_discussed === 'string' 
        ? (data.products_discussed as string).split(',').map(s => s.trim()).filter(Boolean)
        : data.products_discussed,
      samples_given: typeof data.samples_given === 'string'
        ? (data.samples_given as string).split(',').map(s => s.trim()).filter(Boolean)
        : data.samples_given,
      // API expects null if follow_up_date is empty string
      follow_up_date: data.follow_up_date || undefined
    };
    
    const resultAction = await dispatch(createInteraction(processedData));
    if (createInteraction.fulfilled.match(resultAction)) {
      reset();
      // We could add a success toast here
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit(onSubmit)} sx={{ mt: 2 }}>
      {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}
      
      <Grid container spacing={3}>
        <Grid item xs={12} sm={6}>
          <Controller
            name="hcp_id"
            control={control}
            rules={{ required: 'Please select a Healthcare Professional', min: { value: 1, message: 'Select an HCP' } }}
            render={({ field }) => (
              <TextField
                {...field}
                select
                label="Healthcare Professional"
                fullWidth
                error={!!errors.hcp_id}
                helperText={errors.hcp_id?.message}
                disabled={hcpsLoading}
              >
                <MenuItem value={0} disabled>
                  <em>Select HCP</em>
                </MenuItem>
                {hcps.map((hcp) => (
                  <MenuItem key={hcp.id} value={hcp.id}>
                    {hcp.name} ({hcp.speciality}) - {hcp.hospital}
                  </MenuItem>
                ))}
              </TextField>
            )}
          />
        </Grid>
        
        <Grid item xs={12} sm={3}>
          <Controller
            name="date"
            control={control}
            rules={{ required: 'Date is required' }}
            render={({ field }) => (
              <TextField
                {...field}
                label="Date"
                type="date"
                fullWidth
                InputLabelProps={{ shrink: true }}
                error={!!errors.date}
                helperText={errors.date?.message}
              />
            )}
          />
        </Grid>

        <Grid item xs={12} sm={3}>
          <Controller
            name="time"
            control={control}
            rules={{ required: 'Time is required' }}
            render={({ field }) => (
              <TextField
                {...field}
                label="Time"
                type="time"
                fullWidth
                InputLabelProps={{ shrink: true }}
                error={!!errors.time}
                helperText={errors.time?.message}
              />
            )}
          />
        </Grid>

        <Grid item xs={12} sm={4}>
          <Controller
            name="visit_type"
            control={control}
            rules={{ required: 'Visit type is required' }}
            render={({ field }) => (
              <TextField
                {...field}
                select
                label="Visit Type"
                fullWidth
                error={!!errors.visit_type}
                helperText={errors.visit_type?.message}
              >
                {visitTypes.map((type) => (
                  <MenuItem key={type} value={type}>
                    {type}
                  </MenuItem>
                ))}
              </TextField>
            )}
          />
        </Grid>

        <Grid item xs={12} sm={8}>
          <Controller
            name="products_discussed"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="Products Discussed (Comma separated)"
                fullWidth
                placeholder="e.g. Aspirin, Ibuprofen"
              />
            )}
          />
        </Grid>

        <Grid item xs={12} sm={8}>
          <Controller
            name="samples_given"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="Samples Given (Comma separated)"
                fullWidth
                placeholder="e.g. 5x Aspirin 100mg"
              />
            )}
          />
        </Grid>

        <Grid item xs={12} sm={4}>
          <Controller
            name="follow_up_date"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="Follow-up Date (Optional)"
                type="date"
                fullWidth
                InputLabelProps={{ shrink: true }}
              />
            )}
          />
        </Grid>

        <Grid item xs={12}>
          <Controller
            name="feedback"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="Doctor's Feedback"
                fullWidth
                multiline
                rows={2}
              />
            )}
          />
        </Grid>

        <Grid item xs={12}>
          <Controller
            name="notes"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="General Notes"
                fullWidth
                multiline
                rows={3}
              />
            )}
          />
        </Grid>

        <Grid item xs={12}>
          <Box display="flex" justifyContent="flex-end" mt={2}>
            <Button
              type="submit"
              variant="contained"
              color="primary"
              size="large"
              disabled={isLoading || hcpsLoading}
              sx={{ minWidth: 150 }}
            >
              {isLoading ? <CircularProgress size={24} /> : 'Save Interaction'}
            </Button>
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
};
