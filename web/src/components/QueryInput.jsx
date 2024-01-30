import { useState } from 'react'
import { styled } from '@mui/system'
import Stack from '@mui/material/Stack'
import TextField from '@mui/material/TextField'
import InputAdornment from '@mui/material/InputAdornment'
import Button from '@mui/material/Button'
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome'
import SearchIcon from '@mui/icons-material/Search'

const ButtonGenAI = styled(Button)(({ theme }) => ({
  backgroundColor: theme.palette.secondary.main,
  '&:hover': {
    backgroundColor: theme.palette.secondary.light,
  },
  border: 1,
  borderColor: theme.palette.secondary.dark,
  borderRadius: 8,
  color: '#fff'
}));

export default function QueryInput(props) {
  const { onQuerySearch, onQueryGenAI } = props
  const [value, setValue] = useState('')

  return (
    <Stack direction="row" spacing={2}>
      <TextField
        fullWidth
        multiline
        id="mainInput"
        sx={{ pl: 1 }}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={(ev) => {
          if (ev.key === 'Enter') {
            onQuerySearch(value)
            ev.preventDefault()
          }
        }}
        InputProps={{
          endAdornment: (
            <InputAdornment>
              <SearchIcon />
            </InputAdornment>
          ),
        }}
      />
      <ButtonGenAI
        onClick={() => onQueryGenAI(value)}
      >
        <AutoAwesomeIcon />
      </ButtonGenAI>
    </Stack>
  )
}
