import * as React from 'react'
import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import Divider from '@mui/material/Divider'
import CircularProgress from '@mui/material/CircularProgress'
import List from '@mui/material/List'
import ListItemButton from '@mui/material/ListItemButton'

import { ContentBox, ContentBoxTitle } from '../../utils/style/component'
import { useFetchSearch } from '../../utils/hooks'
import ListItemSource from '../Atoms/ListItemSource'

export default function CardSearch(props) {
  const { searchId } = props

  const { search, isLoadingSearch, errorLoadingSearch } =
    useFetchSearch(searchId)
  if (errorLoadingSearch) {
    return <span>Impossible to load the search</span>
  }

  return (
    <ContentBox sx={{ width: '100%' }}>
      {isLoadingSearch ? (
        <CircularProgress />
      ) : (
        <Stack spacing={1} sx={{ m: 1 }}>
          <ContentBoxTitle>{search.query}</ContentBoxTitle>
          <Divider />
          <List dense>
            {search.search_sources?.map((ss) => (
              <ListItemButton sx={{ pt: 0, pb: 0 }}>
                <Typography variant="body2" color="secondary" sx={{ mr: 2, width: '20px', alignContent:'flex-end' }}>
                  {ss.rank}
                </Typography>
                <ListItemSource source={ss.source} />
              </ListItemButton>
            ))}
          </List>
        </Stack>
      )}
    </ContentBox>
  )
}
