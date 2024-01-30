import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import LinearProgress from '@mui/material/LinearProgress'

import { ContentBox } from '../../utils/style/component'

export default function LongProgress(props) {
  const { message } = props
  return (
    <ContentBox display="flex">
      <Stack
        spacing={2}
        justifyContent="center"
        alignItems="center"
        sx={{ width: '100%', p: 4 }}
      >
        <Typography
          variant="subtitle1"
          color="primary"
          align="center"
          sx={{ fontWeight: 'bold' }}
        >
          {message}
        </Typography>
        <LinearProgress sx={{ width: '50%' }} />
      </Stack>
    </ContentBox>
  )
}
