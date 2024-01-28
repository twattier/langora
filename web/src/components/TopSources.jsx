import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import Divider from '@mui/material/Divider'
import {ContentBox} from '../utils/style/component'

export default function TopSources() {
  return (
    <ContentBox sx={{ width: '100%' }}>
      <Stack spacing={1} sx={{ m: 1 }}>
        <Typography
          variant="subtitle1"
          align="center"
          color="primary"
          sx={{ fontWeight: 'bold' }}
        >
          Top Sources
        </Typography>
        <Divider />
        <Typography>Source1</Typography>
        <Typography>Source2</Typography>
        <Typography>Source3</Typography>
        <Typography>Source4</Typography>
        <Typography>Source5</Typography>
      </Stack>
    </ContentBox>
  )
}
