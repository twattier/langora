import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import Divider from '@mui/material/Divider'
import {ContentBox} from '../utils/style/component'

export default function TopSearches() {
  return (
    <ContentBox sx={{ width: '100%'}}>
      <Stack spacing={1} sx={{ m: 1 }}>
        <Typography
          variant="subtitle1"
          align="center"          
          color="primary"
          sx={{ fontWeight: 'bold' }}
        >
          Top Searches
        </Typography>
        <Divider />
        <Typography>Search1</Typography>
        <Typography>Search2</Typography>
        <Typography>Search3</Typography>
        <Typography>Search4</Typography>
        <Typography>Search5</Typography>
      </Stack>
    </ContentBox>
  )
}
