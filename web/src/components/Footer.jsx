import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'

export default function Footer() {
  return (
    <Box display="flex" justifyContent="center" sx={{ mt: 2 }}>
      <Typography variant="caption" align="center" sx={{ fontStyle: 'italic' }}>
        @ Langora 2024
      </Typography>
    </Box>
  )
}
