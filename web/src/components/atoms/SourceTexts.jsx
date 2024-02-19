import Stack from '@mui/material/Stack'
import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'

import { DisplayLines } from '../../utils/display'

export default function ListSources(props) {
  const { sourceTexts } = props

  return (
    <Stack>
      {sourceTexts?.map((text) => (
        <Stack sx={{mt:1}}>
          <Box>
            <Typography sx={{ fontWeight: 'bold' }}>{text.title}</Typography>{' '}
            <Typography>[Suppr]</Typography>
          </Box>
          <DisplayLines text={text.text} />
        </Stack>
      ))}
    </Stack>
  )
}
