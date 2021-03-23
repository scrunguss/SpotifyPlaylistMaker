import { useState, useEffect } from 'react';
import {
  IonHeader,
  IonToolbar,
  IonContent,
  IonIcon,
  IonPage,
  IonFab,
  IonTitle,
  IonList,
  IonItem,
  IonFabButton,
  IonModal,
  IonButton,
  IonButtons,
  IonInput
} from '@ionic/react';
import { add, close } from 'ionicons/icons';
import GroupContainer from '../components/GroupContainer';
import { get } from '../hooks/useGroupStorage';
import { sendRequest } from '../hooks/requestManager';
import './Groups.scss';
import GroupView from '../components/GroupView';
import { getgroups } from 'node:process';

interface Group {
  group_code: string;
  group_name: string;
}

async function getUsersGroups(userId: number | string): Promise<Group[]> {
  const params = {
    spotifyID: userId
  }
/*   console.log("Trying to get groups...");
  console.log("User ID :",userId); */
  sendRequest("GET", "getUsersGroupsBySpotifyID", params, "groups");
  const groups = await get("groups");
 /*  console.log("Groups om getUSersGroups : ",groups);
  console.log("parse : ",JSON.parse(groups)['data']); */
  if(groups !== null && JSON.parse(groups)['success']){
    console.log("returning groups");
    return JSON.parse(groups)['data'];
  }
  /* console.log("returning empty"); */
  return [];
}

const Groups: React.FC = () => {
  const [groups, setGroups] = useState<Group[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [selectedGroup, setSelectedGroup] = useState({group_code: "", group_name: ""});
  const [code, setCode] = useState<string>("");

  const getModal = (group: Group) => {
    setSelectedGroup(group);
    setShowModal(true);
  }

  const joinGroup = (groupCode: string) => {
    const userID = JSON.parse(document.cookie).spotifyID.spotify_id;
    const params = { groupCode: groupCode, userID: userID };
    sendRequest("POST", "addGroupMember", params, "addmember");
  }

  useEffect(() => {
    const currUserID = JSON.parse(document.cookie.split('; ')[0].slice(5)).spotify_id;
    const groups_promise = getUsersGroups(currUserID);
    groups_promise.then((values) => {
      console.log("Groups : ",values);
      if (values !== null) {
        setGroups(values);
        
      }
    }
    );
  }, []);

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Groups</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen>
        <IonModal isOpen={showModal} swipeToClose={true}>
          <IonToolbar>
            <IonTitle>{selectedGroup.group_name}</IonTitle>
            <IonButtons slot="secondary">
              <IonButton onClick={() => setShowModal(false)}>
                <IonIcon icon={close}/>
              </IonButton>
            </IonButtons>
          </IonToolbar>
          <GroupView groupCode={selectedGroup.group_code} groupName={selectedGroup.group_name}/>
        </IonModal>
        <IonFab vertical="top" horizontal="end" slot="fixed" edge>
          <IonFabButton href="./create_group">
            <IonIcon icon={add}/>
          </IonFabButton>
        </IonFab>
        <IonList>
          {groups.map((group, index: number) => (
            <IonItem key={index} onClick={() => getModal(group)}>
              <GroupContainer groupName={group.group_name}/>
            </IonItem>
          ))}
         {/*  <IonItem>
            <IonInput value={code} placeholder="Group code"
              onIonChange={e => setCode(e.detail.value!)}></IonInput>
            <IonButton onClick={() => joinGroup(code)}>Join group with code</IonButton>
          </IonItem> */}
        </IonList>
      </IonContent>
    </IonPage>
  );
};

export default Groups;
