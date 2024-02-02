import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'

import { useFetchKnowledge } from '../../utils/hooks'
import logo from '../../assets/langora.png'
import CommentIcon from '@mui/icons-material/Comment'

export default function Banner() {
  const { knowledge, isLoadingknowledge, errorLoadingknowledge } =
    useFetchKnowledge()

  return (
    <Stack>
      <Box sx={{ pt: 2 }} align="center">
        <img src={logo} alt="langora" height="150px" />
      </Box>
      <Typography variant="h6" color="secondary" sx={{ fontWeight: 'bold', lineHeight: '18px' }}>
        <Stack direction="row" alignItems="center">
          <CommentIcon fontSize="large" sx={{ml:1, mr:1}}/>
          <Box display="block">
            As {knowledge?.agent}.<br /> What can I do for you ?
          </Box>
        </Stack>
      </Typography>
    </Stack>
  )
}
