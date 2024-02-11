import * as React from 'react'
import { useState } from 'react'
import { useParams } from 'react-router-dom'
import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'

import { ContentBox } from '../../utils/style/component'
import NavBar from '../../components/App/NavBar'
import SimilaritySearches from '../../components/Knowledges/SimilaritySearches'
import CardSearch from '../../components/Knowledges/CardSearch'
import SearchIcon from '@mui/icons-material/Search'

import { ActionButton, InputText } from '../../utils/style/component'

export default function Searches(props) {
  const { searchId } = useParams()
  const [valueSearch, setValueSearch] = useState('')
  const [querySearch, setQuerySearch] = useState()
  const onQuerySearch = (query) => {
    setQuerySearch(query)
  }

  const [selectedSearchId, setSelectedSearchId] = useState(searchId)
  const onSelectSearch = (search) => {
    setSelectedSearchId(search.id)
  }

  return (
    <Stack spacing={1} sx={{ p: 1 }}>
      <NavBar selected="searches" />
      <Stack direction="row" spacing={1}>
        <InputText
          sx={{ width: '100%' }}
          onChange={(e) => setValueSearch(e.target.value)}
          onKeyDown={(ev) => {
            if (ev.key === 'Enter' && ev.ctrlKey) {
              onQuerySearch(valueSearch)
              ev.preventDefault()
            }
          }}
        />
        <ActionButton>
          <SearchIcon onClick={() => onQuerySearch(valueSearch)} />
        </ActionButton>
      </Stack>

      {!querySearch ? null : (
        <ContentBox>
          <Box sx={{ p: 1 }}>
            <SimilaritySearches
              query={querySearch}
              onSelectSearch={onSelectSearch}
            />
          </Box>
        </ContentBox>
      )}

      {!selectedSearchId ? null : (
        <CardSearch searchId={selectedSearchId} />
      )}

    </Stack>
  )
}
