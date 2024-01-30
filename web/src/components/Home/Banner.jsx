import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'

import { useFetchKnowledge } from '../../utils/hooks'

export default function Banner() {
  const { knowledge, isLoadingknowledge, errorLoadingknowledge } =
  useFetchKnowledge()

  return (
    <Box display="flex" justifyContent="center">
      <Typography variant="h5" align="center" color="secondary" sx={{ fontWeight: 'bold', p:6 }}>
        {knowledge?.agent}
      </Typography>
    </Box>
  )
}