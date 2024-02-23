import Stack from '@mui/material/Stack'
import ListItemButton from '@mui/material/ListItemButton'
import Typography from '@mui/material/Typography'

export default function ListItemSource(props) {
  const { source } = props

  return (
    <Stack
      direction="row"
      justifyContent="flex-start"
      alignItems="center"
      sx={{ height: 24 }}
    >
      <ListItemButton
        Box
        display="flex"
        sx={{ width: '100%' }}
        onClick={() =>
          (window.location.href = '/knowledges/sources/' + source.id)
        }
      >
        <img
          src={`http://www.google.com/s2/favicons?domain=${source.site}`}
          alt={source.site}
          width="20"
          height="20"
        />
        <Typography variant="body2" sx={{ pl: 1 }}>
          {source.title}
        </Typography>
        {/* <Typography variant="caption" sx={{ pl:1 }}>[{source.site}]</Typography> */}
      </ListItemButton>
    </Stack>
  )
}
