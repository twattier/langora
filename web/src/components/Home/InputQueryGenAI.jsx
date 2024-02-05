import { useState } from 'react'
import { styled } from '@mui/system'
import Stack from '@mui/material/Stack'
import Button from '@mui/material/Button'
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome'

import {InputText, ButtonGenAI} from '../../utils/style/component'

export default function InputQueryGenAI(props) {
  const { onQueryGenAI } = props
  const [value, setValue] = useState('')

  return (
    <Stack direction="row" spacing={1}>
      <InputText
        fullWidth
        multiline
        id="mainInput"
        sx={{ pl: 1}}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={(ev) => {
          if (ev.key === 'Enter' && ev.ctrlKey) {
            onQueryGenAI(value)
            ev.preventDefault()
          }
        }}        
      />
      <ButtonGenAI sx={{height:55}}
        onClick={() => onQueryGenAI(value)}
      >
        <AutoAwesomeIcon />
      </ButtonGenAI>
    </Stack>
  )
}
