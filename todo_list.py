def update_todo_list(console):
    console.todo_list.clear()
    text = console.code_editor.toPlainText()
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if 'TODO:' in line:
            console.todo_list.addItem(f"Line {i + 1}: {line.strip()}")

def goto_todo(console, item):
    line_number = int(item.text().split()[1].strip(':'))
    cursor = console.code_editor.textCursor()
    cursor.setPosition(console.code_editor.document().findBlockByLineNumber(line_number - 1).position())
    console.code_editor.setTextCursor(cursor)
    console.code_editor.setFocus()
