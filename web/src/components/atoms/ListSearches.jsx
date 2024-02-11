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
          onClick={(event) =>
            (window.location.href = '/knowledges/searches/' + search.id)
          }
        >
          <Typography variant="body2">
            <SearchIcon sx={{ mr: 1 }} />
            {`${search.query} [${search.nb_sources}]`}
          </Typography>
        </ListItemButton>
      ))}
    </List>
  )
}
