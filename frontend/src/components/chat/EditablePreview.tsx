import React from 'react';
import { Box, Paper, Typography, TextField, Button, Grid } from '@mui/material';

interface EditablePreviewProps {
  data: any;
  onConfirm: (data: any) => void;
  onCancel: () => void;
}

export const EditablePreview: React.FC<EditablePreviewProps> = ({ data, onConfirm, onCancel }) => {
  const [formData, setFormData] = React.useState(data);

  const handleChange = (field: string, value: string) => {
    setFormData({ ...formData, [field]: value });
  };

  return (
    <Paper elevation={3} sx={{ p: 3, my: 2, border: '2px solid #1976d2' }}>
      <Typography variant="h6" color="primary" gutterBottom>
        Interaction Preview
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        Review and edit the extracted details before saving.
      </Typography>
      
      <Grid container spacing={2}>
        <Grid item xs={12} sm={6}>
          <TextField
            label="HCP Name / ID"
            fullWidth
            value={formData.hcp_id || ''}
            onChange={(e) => handleChange('hcp_id', e.target.value)}
            size="small"
          />
        </Grid>
        <Grid item xs={12} sm={3}>
          <TextField
            label="Date"
            fullWidth
            value={formData.date || ''}
            onChange={(e) => handleChange('date', e.target.value)}
            size="small"
          />
        </Grid>
        <Grid item xs={12} sm={3}>
          <TextField
            label="Time"
            fullWidth
            value={formData.time || ''}
            onChange={(e) => handleChange('time', e.target.value)}
            size="small"
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            label="Visit Type"
            fullWidth
            value={formData.visit_type || ''}
            onChange={(e) => handleChange('visit_type', e.target.value)}
            size="small"
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            label="Follow-up Date"
            fullWidth
            value={formData.follow_up_date || ''}
            onChange={(e) => handleChange('follow_up_date', e.target.value)}
            size="small"
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            label="Products Discussed"
            fullWidth
            value={Array.isArray(formData.products_discussed) ? formData.products_discussed.join(', ') : formData.products_discussed || ''}
            onChange={(e) => handleChange('products_discussed', e.target.value)}
            size="small"
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            label="Feedback"
            fullWidth
            multiline
            rows={2}
            value={formData.feedback || ''}
            onChange={(e) => handleChange('feedback', e.target.value)}
            size="small"
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            label="Notes"
            fullWidth
            multiline
            rows={2}
            value={formData.notes || ''}
            onChange={(e) => handleChange('notes', e.target.value)}
            size="small"
          />
        </Grid>
      </Grid>
      
      <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 3, gap: 2 }}>
        <Button variant="outlined" color="error" onClick={onCancel}>
          Cancel
        </Button>
        <Button variant="contained" color="success" onClick={() => onConfirm(formData)}>
          Confirm & Save
        </Button>
      </Box>
    </Paper>
  );
};
