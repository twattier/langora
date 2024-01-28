import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'

export default function Banner() {
  return (
    <Box display="flex" justifyContent="center">
      <Typography variant="h4" align="center" color="secondary" sx={{ fontWeight: 'bold', p:6 }}>
        Title
      </Typography>
    </Box>
  )
}
