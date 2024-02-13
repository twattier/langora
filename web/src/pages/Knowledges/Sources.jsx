import * as React from 'react'
import { useState } from 'react'
import { useParams } from 'react-router-dom'
import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'

import { ContentBox } from '../../utils/style/component'
import NavBar from '../../components/App/NavBar'
import SearchIcon from '@mui/icons-material/Search'

import { ActionButton, InputText } from '../../utils/style/component'
import SimilaritySources from '../../components/Knowledges/SimilaritySources'
import CardSource from '../../components/Knowledges/CardSource'

export default function Sources() {
  const { sourceId } = useParams()
  const [valueSearch, setValueSearch] = useState('')
  const [querySearch, setQuerySearch] = useState()
  const onQuerySearch = (query) => {
    setQuerySearch(query)
  }

  const [selectedSourceId, setSelectedSourceId] = useState(sourceId)
  const onSelectSource = (source) => {
    setSelectedSourceId(source.id)
  }

  return (
    <Stack spacing={1} sx={{ p: 1 }}>
      <NavBar selected="sources" />
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
            <SimilaritySources
              query={querySearch}
              onSelectSource={onSelectSource}
            />
          </Box>
        </ContentBox>
      )}

      {!selectedSourceId ? null : <CardSource sourceId={selectedSourceId} />}
    </Stack>
  )
}
