"""
Generate a README.md file for all developers that are listed under each category
"""
import os 
import json
from string import Template

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(f'BASE_DIR: {BASE_DIR}')
print('os pwd: ', os.getcwd())

with open(os.path.join(BASE_DIR, 'README_TEMPLATE.md'), 'r') as f:
    README_TEMPLATE = Template(f.read())

def get_category():
    """
    Get category from category.json
    """
    with open(os.path.join(BASE_DIR, 'category.json'), 'r') as f:
        category = json.load(f)
    return category

def get_members(category: str):
    """
    Get members from Base dir/category/members.json
    """
    try:
        with open(os.path.join(BASE_DIR, category, 'members.json'), 'r') as f:
            members_name = json.load(f)
        members = []
        members_name = sorted(members_name)
        for member in members_name:
            with open(os.path.join(BASE_DIR, category, f'{member}'), 'r') as f:
                content = f.read()
                members.append(content.strip())

        return members
    except FileNotFoundError as e:
        print(f' 37 File not found: {os.path.join(BASE_DIR, category, "members.json")}, {e}')
        return []

def get_new_members(category: str):
    """
    Get new members if the name in the base dir/category/member_name.md is not in the members.json
    """
    try:
        with open(os.path.join(BASE_DIR, category, 'members.json'), 'r') as f:
            old_members_name = json.load(f)
        new_members = []
        new_members_name = []
        for member in os.listdir(os.path.join(BASE_DIR, category)):
            if member.endswith('.md'):
                if member not in old_members_name:
                    with open(os.path.join(BASE_DIR, category, member), 'r') as f:
                        content = f.read()
                        new_members.append(content.strip())
                    new_members_name.append(member)
        
        if new_members_name:
            # if there are new members, add them to members.json
            with open(os.path.join(BASE_DIR, category, 'members.json'), 'r') as f:
                members_name = json.load(f)
            members_name.extend(new_members_name)
            with open(os.path.join(BASE_DIR, category, 'members.json'), 'w') as f:
                json.dump(members_name, f, indent=4)
        return new_members
    except FileNotFoundError:
        return []

def get_all_members(category: str):
    """
    Get all members from members.json and new members
    """
    members = get_members(category)
    new_members = get_new_members(category)
    all_members = members + new_members
    return all_members

def generate_readme():
    """
    Generate a README.md file for all developers that are listed under each category
    """
    category = get_category()
    categories_text = ''
    developers_text = ''
    for category_name in category:
        categories_text += f'- [{category_name}](#{category_name})\n'
        developers_text += f'## {category_name}\n\n'
        for count, member in enumerate(get_all_members(category_name)):
            developers_text += f'### Developer {count+1}\n{member}\n\n'
        developers_text += '\n'
    
    readme = README_TEMPLATE.substitute(categories=categories_text, developers=developers_text.strip())
    with open(os.path.join(BASE_DIR, 'README-test.md'), 'w') as f:
        f.write(readme)

if __name__ == '__main__':
    generate_readme()