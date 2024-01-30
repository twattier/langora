import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'

export default function ListItemSource(props) {
  const { source } = props

  return (
    <Stack direction="row" sx={{height:20}} justifyContent="center">
      <Typography variant="body2" sx={{ width: '100%' }}>
        {source.title}
      </Typography>
      <img src={`http://www.google.com/s2/favicons?domain=${source.site}`} alt={source.site} width="18" height="18"/>
      <Typography variant="caption" sx={{ pl:1 }}>{source.site}</Typography>
    </Stack>
  )
}
