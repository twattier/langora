import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import {ContentBox} from '../utils/style/component'

export default function Menu() {
  return (
    <ContentBox display="flex" sx={{pl:4, pt:1, pb:1, mt:1, mb:1}}>
        <Stack direction="row" spacing={4} justifyContent="space-between">
        <Typography variant="h6" color="primary">Menu1</Typography>        
        <Typography variant="h6" color="primary">Menu2</Typography>
        <Typography variant="h6" color="primary">Menu3</Typography>
        <Typography variant="h6" color="primary">Menu4</Typography>
      </Stack>
    </ContentBox>
  )
}
