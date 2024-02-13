import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import List from '@mui/material/List'
import ListItemButton from '@mui/material/ListItemButton'
import SearchIcon from '@mui/icons-material/Search'

export default function ListSearches(props) {
  const { searches } = props

  return (
    <List dense>
      {searches?.map((search) => (
        <ListItemButton
          sx={{ pt: 0, pb: 0 }}
          onClick={() =>
            (window.location.href = '/knowledges/searches/' + search.id)
          }
        >
          <Stack
            direction="row"
            justifyContent="flex-start"
            alignItems="center"
            sx={{ height: 24 }}
          >
            <SearchIcon sx={{ mr: 1 }} />
            <Typography variant="body2">
              {`${search.query}`}
            </Typography>
          </Stack>
        </ListItemButton>
      ))}
    </List>
  )
}
